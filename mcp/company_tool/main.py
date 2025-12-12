# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os, json
# from groq import Groq
# from typing import Dict, Any

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# router = APIRouter()

# class CompanyInput(BaseModel):
#     company: str


# def safe_parse_json(text: str) -> Dict[str, Any]:
#     """Try to extract and parse JSON even if the LLM adds extra text."""
#     try:
#         return json.loads(text)
#     except:
#         pass

#     try:
#         start = text.index("{")
#         end = text.rindex("}") + 1
#         block = text[start:end]
#         return json.loads(block)
#     except Exception as e:
#         raise ValueError("Failed to parse JSON from model output") from e


# @router.post("/tools/company_enrich")
# def enrich_company(payload: CompanyInput):

#     prompt = f"""
# Analyze the company name: "{payload.company}"

# Return ONLY a JSON object:

# {{
#   "company": "{payload.company}",
#   "is_real": true|false,
#   "size": "small"|"medium"|"large"|"unknown",
#   "industry": "string",
#   "website": "https://..." or null,
#   "score": 0.0,
#   "reason": "short explanation"
# }}
# """

#     # ✔ STABLE GROQ MODEL
#     model_name = "llama-3.1-8b-instant"

#     try:
#         resp = client.chat.completions.create(
#             model=model_name,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.1
#         )
#     except Exception as e:
#         raise HTTPException(status_code=502, detail=f"LLM request failed: {e}")

#     try:
#         raw_output = resp.choices[0].message.content
#     except:
#         raise HTTPException(status_code=502, detail="Invalid model response format")

#     # --- Parse JSON safely ---
#     try:
#         result = safe_parse_json(raw_output)
#     except:
#         result = {
#             "company": payload.company,
#             "is_real": False,
#             "size": "unknown",
#             "industry": "unknown",
#             "website": None,
#             "score": 0.5,
#             "reason": "failed to parse model output"
#         }

#     # --- Clean + normalize output ---
#     cleaned = {
#         "company": result.get("company", payload.company),
#         "is_real": bool(result.get("is_real", False)),
#         "size": result.get("size", "unknown"),
#         "industry": result.get("industry", "unknown"),
#         "website": result.get("website", None),
#         "score": 0.5,
#         "reason": result.get("reason", "No reason provided")
#     }

#     # Score normalization
#     try:
#         score = float(result.get("score", 0.5))
#         cleaned["score"] = max(0.0, min(1.0, score))
#     except:
#         cleaned["score"] = 0.5

#     return cleaned


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os, json, re
from typing import Dict, Any
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

router = APIRouter()


class CompanyInput(BaseModel):
    company: str


# -------------------------------
#  FAST RULE-BASED CHECKS (NO LLM)
# -------------------------------
FAKE_COMPANY_KEYWORDS = {
    "test", "demo", "sample", "abc", "xyz", 
    "company", "testing", "placeholder", "fake"
}

def looks_fake_company(name: str) -> bool:
    n = name.lower().strip()
    if len(n) < 3:
        return True
    if n in FAKE_COMPANY_KEYWORDS:
        return True
    if n.isnumeric():
        return True
    if any(char.isdigit() for char in n):
        return True
    return False


# -------------------------------
#  SAFE JSON EXTRACTION
# -------------------------------
def safe_parse_json(text: str) -> Dict[str, Any]:
    """Extract JSON from LLM output safely."""
    text = text.strip()

    # Try direct load
    try:
        return json.loads(text)
    except:
        pass

    # Remove markdown fences
    clean = re.sub(r"```json|```", "", text).strip()

    # Extract JSON block
    try:
        start = clean.index("{")
        end = clean.rindex("}") + 1
        block = clean[start:end]
        return json.loads(block)
    except:
        return None


# -------------------------------
#  ROUTE: COMPANY ENRICHMENT
# -------------------------------
@router.post("/tools/company_enrich")
def enrich_company(payload: CompanyInput):

    company = payload.company.strip()

    # -------------------------------
    # 1️⃣ RULE-BASED EARLY RETURN  
    # -------------------------------
    if looks_fake_company(company):
        return {
            "company": company,
            "is_real": False,
            "size": "unknown",
            "industry": "unknown",
            "website": None,
            "score": 0.1,
            "reason": "Company name appears generic, placeholder, or invalid."
        }

    # -------------------------------
    # 2️⃣ LLM PROMPT
    # -------------------------------
    prompt = f"""
Analyze the company name: "{company}"

Identify:
- is_real: true or false
- size: small | medium | large | unknown
- industry: string or "unknown"
- website: URL or null
- score: 0.0 to 1.0 (trust/confidence)
- reason: short explanation

Respond ONLY in proper JSON:

{{
  "company": "{company}",
  "is_real": true,
  "size": "medium",
  "industry": "technology",
  "website": "https://example.com",
  "score": 0.0,
  "reason": ""
}}
"""

    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    raw = resp.choices[0].message.content

    # -------------------------------
    # 3️⃣ TRY PARSING JSON SAFELY
    # -------------------------------
    parsed = safe_parse_json(raw)

    if parsed is None:
        # Fallback if the model broke JSON
        return {
            "company": company,
            "is_real": False,
            "size": "unknown",
            "industry": "unknown",
            "website": None,
            "score": 0.4,
            "reason": "Failed to parse JSON from the model output."
        }

    # -------------------------------
    # 4️⃣ NORMALIZE + VALIDATE OUTPUT
    # -------------------------------
    cleaned = {
        "company": parsed.get("company", company),
        "is_real": bool(parsed.get("is_real", False)),
        "size": parsed.get("size", "unknown"),
        "industry": parsed.get("industry", "unknown"),
        "website": parsed.get("website", None),
        "reason": parsed.get("reason", "No explanation provided")
    }

    # Score normalization
    try:
        score = float(parsed.get("score", 0.5))
        cleaned["score"] = max(0.0, min(1.0, score))
    except:
        cleaned["score"] = 0.5

    return cleaned

# from fastapi import APIRouter
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os, json
# from groq import Groq

# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# router = APIRouter()

# class NameInput(BaseModel):
#     name: str

# @router.post("/tools/name_check")
# def check_name(payload: NameInput):

#     prompt = f"""
#     Analyze this name: "{payload.name}"

#     You must determine:
#     - is_real: true or false (is it a real human name?)
#     - score: trust score between 0 and 1
#     - suspicion: one of ["normal", "rare", "bot_like", "fake"]
#     - reason: short explanation

#     Respond ONLY with valid JSON in this format:

#     {{
#         "name": "{payload.name}",
#         "is_real": true,
#         "score": 0.0,
#         "suspicion": "",
#         "reason": ""
#     }}
#     """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",   # Updated & stable Groq model
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2
#     )

#     raw_output = response.choices[0].message.content

#     # ---- Safe JSON extraction ----
#     try:
#         result = json.loads(raw_output)
#     except:
#         try:
#             json_part = raw_output[raw_output.index("{"): raw_output.rindex("}") + 1]
#             result = json.loads(json_part)
#         except:
#             result = {
#                 "name": payload.name,
#                 "is_real": False,
#                 "score": 0.4,
#                 "suspicion": "unsure",
#                 "reason": "Model returned invalid JSON"
#             }

#     # ---- Ensure aggregator compatibility ----
#     if "score" not in result:
#         # If missing, estimate score based on suspicion
#         suspicion = result.get("suspicion", "unsure")
#         result["score"] = {
#             "normal": 0.9,
#             "rare": 0.6,
#             "bot_like": 0.3,
#             "fake": 0.1,
#             "unsure": 0.4
#         }.get(suspicion, 0.4)

#     if "reason" not in result:
#         result["reason"] = "Auto-generated reasoning"

#     return result



from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import os, json, re
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

router = APIRouter()


class NameInput(BaseModel):
    name: str


# ---------- RULE-BASED PRE-CHECK (FAST, NO LLM) ----------
def is_test_name(name: str) -> bool:
    test_keywords = ["test", "demo", "sample", "xyz", "abc", "tester", "dummy"]
    return name.lower().strip() in test_keywords


def looks_fake_name(name: str) -> bool:
    name = name.strip().lower()
    if len(name) < 2:
        return True
    if name.isnumeric():
        return True
    if any(char.isdigit() for char in name):
        return True
    if name in ["asd", "qwerty", "zzz"]:
        return True
    return False


@router.post("/tools/name_check")
def check_name(payload: NameInput):

    name = payload.name.strip()

    # -------------------------------------------
    # 1️⃣ RULE-BASED FILTER BEFORE LLM (FREE)
    # -------------------------------------------
    if is_test_name(name):
        return {
            "name": name,
            "is_real": False,
            "score": 0.1,
            "suspicion": "fake",
            "reason": "Common placeholder/test name used in development."
        }

    if looks_fake_name(name):
        return {
            "name": name,
            "is_real": False,
            "score": 0.2,
            "suspicion": "fake",
            "reason": "Name appears synthetic or invalid."
        }

    # -------------------------------------------
    # 2️⃣ LLM-BASED ANALYSIS
    # -------------------------------------------
    prompt = f"""
    Analyze the following human name:

    NAME: "{name}"

    Determine:
    - is_real: true or false
    - score: trust score between 0 and 1
    - suspicion: one of ["normal", "rare", "bot_like", "fake"]
    - reason: short explanation

    Respond ONLY with valid JSON in this format:

    {{
        "name": "{name}",
        "is_real": true,
        "score": 0.0,
        "suspicion": "",
        "reason": ""
    }}

    Do NOT include markdown, comments, or text outside JSON.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw = response.choices[0].message.content.strip()

    # -------------------------------------------
    # 3️⃣ SAFE JSON EXTRACTION (PREVENT CRASHES)
    # -------------------------------------------
    try:
        result = json.loads(raw)
    except:
        try:
            clean = re.sub(r"```json|```", "", raw).strip()
            start = clean.find("{")
            end = clean.rfind("}")
            if start != -1 and end != -1:
                result = json.loads(clean[start:end + 1])
            else:
                raise ValueError("JSON not found")
        except:
            # Fallback when model breaks JSON
            return {
                "name": name,
                "is_real": False,
                "score": 0.4,
                "suspicion": "unsure",
                "reason": "Model returned invalid JSON"
            }

    # -------------------------------------------
    # 4️⃣ ENSURE COMPLETE + NORMALIZED OUTPUT
    # -------------------------------------------
    result.setdefault("name", name)
    result.setdefault("is_real", False)
    result.setdefault("suspicion", "unsure")

    # Score normalization
    suspicion = result.get("suspicion", "unsure")
    result["score"] = {
        "normal": 0.9,
        "rare": 0.6,
        "bot_like": 0.3,
        "fake": 0.1,
        "unsure": 0.4
    }.get(suspicion, 0.4)

    result.setdefault("reason", "No explanation provided")

    return result

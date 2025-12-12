# from fastapi import APIRouter
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# from groq import Groq
# from email_validator import validate_email, EmailNotValidError
# import json

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# router = APIRouter()


# class EmailInput(BaseModel):
#     email: str


# @router.post("/tools/email_reputation")
# def check_email(payload: EmailInput):

#     # 1. HARD VALIDATION (Save tokens)
#     try:
#         # Check syntax, deliverability, domain existence
#         v = validate_email(payload.email, check_deliverability=True)
#         # normalized_email = v.normalized
#     except EmailNotValidError as e:
#         # Fast fail if invalid
#         return {
#             "email": payload.email,
#             "type": "invalid",
#             "score": 0.0,
#             "is_likely_genuine": False,
#             "reason": str(e)
#         }

#     # 2. LLM ANALYSIS

#     prompt = f"""
#     Analyze the email address: {payload.email}

#     Classify the email with:
#     - type: business, personal, spammy, disposable, bot-like
#     - score: trust score (0 to 1)
#     - is_likely_genuine: true or false
#     - reason: short explanation

#     Return ONLY valid JSON:
#     {{
#         "email": "{payload.email}",
#         "type": "",
#         "score": 0.0,
#         "is_likely_genuine": false,
#         "reason": ""
#     }}
#     """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",   # ✔ Updated model
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2
#     )

#     raw = response.choices[0].message.content

#     # ---------- Safe JSON extraction ----------
#     try:
#         data = json.loads(raw)
#     except Exception:
#         try:
#             json_str = raw[raw.index("{"): raw.rindex("}") + 1]
#             data = json.loads(json_str)
#         except Exception:
#             data = {
#                 "email": payload.email,
#                 "type": "unknown",
#                 "score": 0.5,
#                 "is_likely_genuine": False,
#                 "reason": "Model returned invalid JSON"
#             }

#     # Ensure required field for aggregator
#     if "score" not in data:
#         data["score"] = 0.5

#     return data




from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Groq
from email_validator import validate_email, EmailNotValidError
import json

load_dotenv()

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class EmailInput(BaseModel):
    email: str


DISPOSABLE_DOMAINS = {
    "mailinator.com", "tempmail.com", "10minutemail.com",
    "dispostable.com", "fakeinbox.com"
}


@router.post("/tools/email_reputation")
def check_email(payload: EmailInput):

    email = payload.email

    # -------------------------------------------
    # 1️⃣ BASIC HARD VALIDATION (no LLM cost)
    # -------------------------------------------
    try:
        validation = validate_email(email, check_deliverability=True)
        normalized = validation.normalized
    except EmailNotValidError as e:
        return {
            "email": email,
            "type": "invalid",
            "score": 0.0,
            "is_likely_genuine": False,
            "reason": str(e)
        }

    domain = normalized.split("@")[-1]

    # Check for known disposable domains
    if domain in DISPOSABLE_DOMAINS:
        return {
            "email": email,
            "type": "disposable",
            "score": 0.1,
            "is_likely_genuine": False,
            "reason": "Disposable domain detected"
        }

    # -------------------------------------------
    # 2️⃣ LLM ANALYSIS (only when email is valid)
    # -------------------------------------------
    prompt = f"""
    Analyze this email and classify it:

    Email: {email}

    Output ONLY a JSON object with EXACTLY these fields:

    {{
      "email": "{email}",
      "type": "business | personal | spammy | disposable | bot | unknown",
      "score": 0.0,
      "is_likely_genuine": false,
      "reason": "short explanation"
    }}

    Ensure the JSON is VALID and contains no extra text.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()

        # -------------------------------------------
        # 3️⃣ Robust JSON parsing (never fails)
        # -------------------------------------------
        try:
            data = json.loads(raw)
        except:
            try:
                json_str = raw[raw.index("{"): raw.rindex("}") + 1]
                data = json.loads(json_str)
            except:
                # Final fallback
                data = {
                    "email": email,
                    "type": "unknown",
                    "score": 0.5,
                    "is_likely_genuine": False,
                    "reason": "Failed to parse model response"
                }

    except Exception as e:
        # LLM API failure fallback
        data = {
            "email": email,
            "type": "unknown",
            "score": 0.4,
            "is_likely_genuine": False,
            "reason": f"LLM error: {e}"
        }

    # Ensure mandatory fields exist
    data.setdefault("email", email)
    data.setdefault("score", 0.5)
    data.setdefault("type", "unknown")
    data.setdefault("is_likely_genuine", False)
    data.setdefault("reason", "No reason provided")

    return data

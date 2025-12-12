# from fastapi import APIRouter
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os, json
# from groq import Groq

# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# router = APIRouter()

# class MessageInput(BaseModel):
#     message: str

# @router.post("/tools/intent")
# def intent_analysis(payload: MessageInput):

#     prompt = f"""
#     Analyze the following customer message:
#     "{payload.message}"

#     Determine:
#     - intent: buying, demo, pricing, support, complaint, spam, unsure
#     - urgency: number from 0 to 1
#     - quality: number from 0 to 1
#     - spam_probability: number from 0 to 1

#     You must also provide:
#     - score: overall trust/intent confidence (0 to 1)
#     - reason: short explanation of your interpretation

#     Respond ONLY with valid JSON in this exact format:

#     {{
#         "intent": "",
#         "urgency": 0.0,
#         "quality": 0.0,
#         "spam_probability": 0.0,
#         "score": 0.0,
#         "reason": ""
#     }}
#     """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",   # UPDATED Groq model
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
#             # Fallback if model output fails
#             result = {
#                 "intent": "unsure",
#                 "urgency": 0.3,
#                 "quality": 0.3,
#                 "spam_probability": 0.5,
#                 "score": 0.3,
#                 "reason": "Model returned invalid JSON"
#             }

#     # ---- Ensuring aggregator compatibility ----
#     if "score" not in result:
#         result["score"] = (1 - result.get("spam_probability", 0.5))  # heuristic

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


class MessageInput(BaseModel):
    message: str


def looks_spammy(text: str) -> bool:
    """Very cheap rule-based spam detection before LLM call."""
    t = text.lower()

    spam_words = [
        "free", "offer", "buy now", "click here", "limited time",
        "winner", "congratulations", "earn money", "guarantee"
    ]

    if len(text.strip()) < 3:
        return True

    return any(w in t for w in spam_words)


@router.post("/tools/intent")
def intent_analysis(payload: MessageInput):

    msg = payload.message.strip()

    # -----------------------------------------
    # 1️⃣ Short text / obvious spam → NO LLM call 
    # -----------------------------------------
    if len(msg) < 5 or looks_spammy(msg):
        return {
            "intent": "spam" if looks_spammy(msg) else "unsure",
            "urgency": 0.1,
            "quality": 0.1,
            "spam_probability": 0.9 if looks_spammy(msg) else 0.5,
            "score": 0.2,
            "reason": "Message too short or contains spam-like patterns."
        }

    # -----------------------------------------
    # 2️⃣ LLM prompt for real analysis
    # -----------------------------------------
    prompt = f"""
    Analyze the customer message below:

    MESSAGE:
    "{msg}"

    Determine the following values:

    - intent: "buying", "demo", "pricing", "support", "complaint", "spam", "unsure"
    - urgency: (0 to 1)
    - quality: (0 to 1)
    - spam_probability: (0 to 1)
    - score: overall likelihood this is a genuine and meaningful inquiry
    - reason: short explanation

    Respond ONLY with this JSON format:

    {{
        "intent": "",
        "urgency": 0.0,
        "quality": 0.0,
        "spam_probability": 0.0,
        "score": 0.0,
        "reason": ""
    }}

    Do NOT add text, markdown, or comments outside the JSON.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        raw = response.choices[0].message.content.strip()

        # -----------------------------------------
        # 3️⃣ Safe JSON extraction
        # -----------------------------------------
        try:
            result = json.loads(raw)
        except:
            clean = re.sub(r"```json|```", "", raw).strip()
            start = clean.find("{")
            end = clean.rfind("}")
            if start != -1 and end != -1:
                result = json.loads(clean[start:end + 1])
            else:
                raise ValueError("No JSON found")

    except Exception as e:
        # -----------------------------------------
        # 4️⃣ LLM failed → fallback structure
        # -----------------------------------------
        result = {
            "intent": "unsure",
            "urgency": 0.3,
            "quality": 0.3,
            "spam_probability": 0.5,
            "score": 0.3,
            "reason": f"LLM error: {str(e)}"
        }

    # -----------------------------------------
    # 5️⃣ Ensure all required fields exist
    # -----------------------------------------
    result.setdefault("intent", "unsure")
    result.setdefault("urgency", 0.0)
    result.setdefault("quality", 0.0)
    result.setdefault("spam_probability", 0.5)
    result.setdefault("score", 1 - result.get("spam_probability", 0.5))
    result.setdefault("reason", "No explanation provided")

    return result

from fastapi import APIRouter
from pydantic import BaseModel
import phonenumbers
from dotenv import load_dotenv
import os, json
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

router = APIRouter()

class PhoneInput(BaseModel):
    phone: str

@router.post("/tools/phone_check")
def check_phone(payload: PhoneInput):

    number = payload.phone

    # -------- BASIC CHECK USING phonenumbers --------
    try:
        parsed = phonenumbers.parse(number, None)
        valid = phonenumbers.is_valid_number(parsed)
        region = phonenumbers.region_code_for_number(parsed)
    except:
        valid = False
        region = None

    # -------- LLM PROMPT --------
    prompt = f"""
    You are a strictly JSON-only API. 
    Analyze the phone number: "{number}"
    
    TASK:
    Determine if this phone number is GENUINE (real, reachable) or FAKE/DUMMY.
    
    RULES:
    1. Output MUST be a single valid JSON object.
    2. DO NOT write any python code or explanations outside the JSON.
    3. REJECT sequential (123456) or repeated digits (999999).
    
    RESPONSE FORMAT:
    {{
        "score": 0.95,
        "is_genuine": true,
        "type": "mobile",
        "reason": "Valid format, not a dummy pattern"
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",       # UPDATED MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content
    print(f"DEBUG LLM OUTPUT: {raw_output}")  # 🔥 Debugging

    # -------- SAFE JSON EXTRACTION --------
    import re
    try:
        # Try raw parse
        result = json.loads(raw_output)
    except:
        try:
            # Remove markdown code blocks if present
            clean_text = re.sub(r"```json\s*|\s*```", "", raw_output).strip()
            # Try to find the first '{' and last '}'
            start = clean_text.find("{")
            end = clean_text.rfind("}")
            if start != -1 and end != -1:
                json_str = clean_text[start:end+1]
                result = json.loads(json_str)
            else:
                raise ValueError("No JSON found")
        except Exception as e:
            print(f"JSON PARSE ERROR: {e}")
            result = {
                "score": 0.5,
                "is_genuine": False,
                "type": "unknown",
                "reason": f"Model returned invalid JSON. Raw: {raw_output[:50]}..."
            }

    # -------- ENSURE aggregator compatibility --------
    if "score" not in result:
        result["score"] = 0.5

    if "is_genuine" not in result:
        # Fallback logic
        result["is_genuine"] = result.get("score", 0) > 0.6

    if "reason" not in result:
        result["reason"] = "Auto-generated reasoning"

    # -------- ADD phonenumbers metadata --------
    result["parsed_valid"] = valid
    result["region"] = region

    return result

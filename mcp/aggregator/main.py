from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

# ---------------------------------------------------
# Incoming Model From Agents
# ---------------------------------------------------
class Signals(BaseModel):
    lead_id: int

    email: Dict[str, Any] = {}
    phone: Dict[str, Any] = {}
    name: Dict[str, Any] = {}
    company: Dict[str, Any] = {}
    message: Dict[str, Any] = {}


# ---------------------------------------------------
# Safe score extraction helper
# ---------------------------------------------------
def safe_score(value) -> float:
    """
    Ensure score is always a float between 0 and 1.
    """
    try:
        score = float(value)
        if score < 0: return 0.0
        if score > 1: return 1.0
        return score
    except:
        return 0.0


# ---------------------------------------------------
# Weighted Score Logic
# ---------------------------------------------------
def calculate_score(signals: Signals):

    email_score = safe_score(signals.email.get("score"))
    phone_score = safe_score(signals.phone.get("score"))
    name_score = safe_score(signals.name.get("score"))
    company_score = safe_score(signals.company.get("score"))
    message_score = safe_score(signals.message.get("score"))

    weights = {
        "email": 0.30,
        "phone": 0.20,
        "name": 0.10,
        "company": 0.25,
        "message": 0.15,
    }

    total = (
        email_score * weights["email"]
        + phone_score * weights["phone"]
        + name_score * weights["name"]
        + company_score * weights["company"]
        + message_score * weights["message"]
    )

    total = round(max(0.0, min(1.0, total)), 2)

    # Decision based on score
    if total >= 0.75:
        decision = "QUALIFIED"
    elif total >= 0.45:
        decision = "IN_PROGRESS"
    else:
        decision = "NOT_QUALIFIED"

    return total, decision


# ---------------------------------------------------
# AGGREGATOR ENDPOINT
# ---------------------------------------------------
@router.post("/tools/aggregate")
def aggregate(signals: Signals):

    total_score, decision = calculate_score(signals)

    return {
        "lead_id": signals.lead_id,
        "total_score": total_score,
        "decision": decision,

        # Raw component scores for debugging
        "email_score": safe_score(signals.email.get("score")),
        "phone_score": safe_score(signals.phone.get("score")),
        "name_score": safe_score(signals.name.get("score")),
        "company_score": safe_score(signals.company.get("score")),
        "message_score": safe_score(signals.message.get("score")),
    }

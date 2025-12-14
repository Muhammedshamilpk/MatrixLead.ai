from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List

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
# Risk Flag Detection
# ---------------------------------------------------
def detect_risk_flags(signals: Signals) -> List[str]:
    """
    Detect potential risk factors in the lead data.
    Returns a list of risk flag descriptions.
    """
    risk_flags = []
    
    # Email risks
    email_type = signals.email.get("type", "").lower()
    if email_type in ["disposable", "spammy", "bot", "invalid"]:
        risk_flags.append(f"email_{email_type}")
    
    email_genuine = signals.email.get("is_likely_genuine", True)
    if not email_genuine:
        risk_flags.append("email_not_genuine")
    
    # Phone risks
    phone_valid = signals.phone.get("is_valid", True)
    if not phone_valid:
        risk_flags.append("phone_invalid")
    
    phone_type = signals.phone.get("type", "").lower()
    if phone_type == "voip":
        risk_flags.append("phone_voip")
    
    # Name risks
    name_valid = signals.name.get("is_valid", True)
    if not name_valid:
        risk_flags.append("name_suspicious")
    
    # Company risks
    company_exists = signals.company.get("exists", True)
    if not company_exists:
        risk_flags.append("company_not_found")
    
    # Message risks
    message_intent = signals.message.get("intent", "").lower()
    if message_intent in ["spam", "irrelevant", "unclear"]:
        risk_flags.append(f"message_{message_intent}")
    
    return risk_flags


# ---------------------------------------------------
# Confidence Calculation
# ---------------------------------------------------
def calculate_confidence(signals: Signals, risk_flags: List[str]) -> float:
    """
    Calculate confidence level based on data completeness and quality.
    Returns a value between 0 and 1.
    """
    confidence = 1.0
    
    # Reduce confidence for missing data
    if not signals.email or signals.email.get("score", 0) == 0:
        confidence -= 0.15
    if not signals.phone or signals.phone.get("score", 0) == 0:
        confidence -= 0.10
    if not signals.company or signals.company.get("score", 0) == 0:
        confidence -= 0.15
    if not signals.message or signals.message.get("score", 0) == 0:
        confidence -= 0.10
    
    # Reduce confidence for each risk flag
    confidence -= len(risk_flags) * 0.08
    
    return round(max(0.0, min(1.0, confidence)), 2)


# ---------------------------------------------------
# Industry and Company Analysis
# ---------------------------------------------------
HIGH_VALUE_INDUSTRIES = {
    "technology", "software", "saas", "fintech", "finance", 
    "healthcare", "biotech", "pharmaceutical", "enterprise",
    "consulting", "legal", "insurance", "real estate"
}

URGENCY_KEYWORDS = {
    "urgent", "asap", "immediately", "now", "today", "quickly",
    "deadline", "time-sensitive", "priority", "critical"
}

BUYING_INTENT_KEYWORDS = {
    "purchase", "buy", "pricing", "quote", "proposal", "demo",
    "trial", "subscription", "contract", "budget", "cost",
    "looking for", "need", "require", "interested in"
}


def analyze_industry_value(signals: Signals) -> float:
    """
    Analyze company industry and return value multiplier.
    Returns 0.0 to 0.15 bonus.
    """
    industry = signals.company.get("industry", "").lower()
    
    for high_value in HIGH_VALUE_INDUSTRIES:
        if high_value in industry:
            return 0.10  # High-value industry bonus
    
    if industry and industry != "unknown":
        return 0.05  # Any known industry gets small bonus
    
    return 0.0


def analyze_company_size(signals: Signals) -> float:
    """
    Analyze company size and return multiplier.
    Returns 0.0 to 0.10 bonus.
    """
    size = signals.company.get("size", "").lower()
    
    if size == "large":
        return 0.10  # Enterprise clients are valuable
    elif size == "medium":
        return 0.07
    elif size == "small":
        return 0.03
    
    return 0.0


def analyze_message_intent(signals: Signals) -> dict:
    """
    Analyze message for buying intent and urgency.
    Returns dict with urgency_score and intent_score.
    """
    message = signals.message.get("message", "").lower() if isinstance(signals.message.get("message"), str) else ""
    intent = signals.message.get("intent", "").lower()
    
    urgency_score = 0.0
    intent_score = 0.0
    
    # Check for urgency keywords
    urgency_count = sum(1 for keyword in URGENCY_KEYWORDS if keyword in message)
    if urgency_count > 0:
        urgency_score = min(0.08, urgency_count * 0.03)
    
    # Check for buying intent
    buying_count = sum(1 for keyword in BUYING_INTENT_KEYWORDS if keyword in message)
    if buying_count > 0:
        intent_score = min(0.10, buying_count * 0.04)
    
    # Boost for positive intent classification
    if intent in ["interested", "buying", "qualified", "hot"]:
        intent_score += 0.05
    
    return {
        "urgency_score": urgency_score,
        "intent_score": intent_score
    }


# ---------------------------------------------------
# Enhanced Weighted Score Logic with Multi-Factor Analysis
# ---------------------------------------------------
def calculate_score(signals: Signals, risk_flags: List[str]):
    """
    Calculate weighted score with:
    - Multi-factor analysis (industry, company size, intent)
    - Dynamic penalties for risk factors
    - Bonuses for high-quality signal combinations
    - More granular decision tiers
    """
    email_score = safe_score(signals.email.get("score"))
    phone_score = safe_score(signals.phone.get("score"))
    name_score = safe_score(signals.name.get("score"))
    company_score = safe_score(signals.company.get("score"))
    message_score = safe_score(signals.message.get("score"))

    # Enhanced weights - company and email are most important
    weights = {
        "email": 0.28,
        "phone": 0.12,
        "name": 0.08,
        "company": 0.32,  # Increased company weight
        "message": 0.20,  # Increased message weight
    }

    base_score = (
        email_score * weights["email"]
        + phone_score * weights["phone"]
        + name_score * weights["name"]
        + company_score * weights["company"]
        + message_score * weights["message"]
    )

    # Industry and company analysis bonuses
    industry_bonus = analyze_industry_value(signals)
    size_bonus = analyze_company_size(signals)
    
    # Message intent analysis
    intent_analysis = analyze_message_intent(signals)
    urgency_bonus = intent_analysis["urgency_score"]
    buying_intent_bonus = intent_analysis["intent_score"]

    # Apply all bonuses
    total = base_score + industry_bonus + size_bonus + urgency_bonus + buying_intent_bonus
    
    # Enhanced risk penalty calculation
    # Critical risks (email/phone invalid) have higher penalty
    critical_risks = [r for r in risk_flags if any(x in r for x in ["invalid", "disposable", "bot", "spam"])]
    minor_risks = [r for r in risk_flags if r not in critical_risks]
    
    risk_penalty = (len(critical_risks) * 0.08) + (len(minor_risks) * 0.03)
    total -= risk_penalty
    
    # Combination bonuses for high-quality signals
    if email_score >= 0.85 and company_score >= 0.85:
        total += 0.06  # Strong email + company combo
    elif email_score >= 0.75 and company_score >= 0.75:
        total += 0.03
    
    if message_score >= 0.80 and company_score >= 0.75:
        total += 0.04  # Clear intent from good company
    
    # Business email bonus (not personal)
    email_type = signals.email.get("type", "").lower()
    if email_type == "business" and email_score >= 0.7:
        total += 0.05
    
    # Company verification bonus
    if signals.company.get("exists", False) and signals.company.get("website"):
        total += 0.04
    
    # High Intent Bonus (compensates for personal email)
    if buying_intent_bonus >= 0.04 and urgency_bonus >= 0.04:
        total += 0.08  # Strong buying signal bonus to help personal emails qualify

    # Clamp to 0-1 range
    total = round(max(0.0, min(1.0, total)), 2)

    # Enhanced multi-tier decision logic with stricter thresholds
    # REMOVED email_type == "business" requirement to allow strong personal leads to be HOT
    if total >= 0.85 and len(critical_risks) == 0:
        decision = "HOT"  # Immediate high-priority contact
    elif total >= 0.70 and len(critical_risks) == 0:
        decision = "QUALIFIED"  # Contact within 24 hours
    elif total >= 0.55 and len(critical_risks) <= 1:
        decision = "WARM"  # Contact within 48 hours. Lowered to 55 to capture more valid personal emails.
    elif total >= 0.45:
        decision = "NURTURE"  # Add to nurture campaign
    elif total >= 0.35:
        decision = "REVIEW"  # Manual review needed
    else:
        decision = "NOT_QUALIFIED"  # Reject

    return total, decision


# ---------------------------------------------------
# AGGREGATOR ENDPOINT
# ---------------------------------------------------
@router.post("/tools/aggregate")
def aggregate(signals: Signals):
    """
    Enhanced aggregation with risk detection and confidence scoring.
    """
    # Detect risk flags
    risk_flags = detect_risk_flags(signals)
    
    # Calculate confidence
    confidence = calculate_confidence(signals, risk_flags)
    
    # Calculate score and decision
    total_score, decision = calculate_score(signals, risk_flags)

    return {
        "lead_id": signals.lead_id,
        "total_score": total_score,
        "decision": decision,
        "confidence": confidence,
        "risk_flags": risk_flags,

        # Raw component scores for debugging
        "email_score": safe_score(signals.email.get("score")),
        "phone_score": safe_score(signals.phone.get("score")),
        "name_score": safe_score(signals.name.get("score")),
        "company_score": safe_score(signals.company.get("score")),
        "message_score": safe_score(signals.message.get("score")),
        
        # Additional context
        "email_type": signals.email.get("type", "unknown"),
        "company_exists": signals.company.get("exists", False),
        "message_intent": signals.message.get("intent", "unknown"),
    }

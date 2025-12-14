# qualification_graph.py

def run_qualification(payload: dict):
    """
    Simple AI-style logic to qualify leads automatically.
    """

    name = payload.get("name")
    company = payload.get("company")
    # message contains the full form narrative including budget, timeline, etc.
    message = payload.get("message", "") or ""

    score = 0
    decision = "NURTURE"
    confidence = 0.5

    # ----------------------------------------
    # "Smart" Simulation Logic based on Keywords
    # ----------------------------------------

    # 1. Budget Scoring
    if "$100k+" in message:
        score += 40
    elif "$50k-100k" in message:
        score += 30
    elif "$10k-50k" in message:
        score += 15
    elif "No Budget" in message:
        score -= 10

    # 2. Timeline Scoring
    if "ASAP" in message:
        score += 30
    elif "1-3 Months" in message:
        score += 20
    elif "3-6 Months" in message:
        score += 10
    elif "Just Browsing" in message:
        score -= 20

    # 3. Authority Scoring
    if "Decision Maker" in message:
        score += 20
    elif "Champion" in message:
        score += 15
    elif "Influencer" in message:
        score += 10

    # 4. Company Size Scoring (Enterprise bonus)
    if "1000+" in message or "201-1000" in message:
        score += 10
        
    # 5. Base Score for valid contact info
    if name and company:
        score += 5

    # Normalize Score (Cap at 100, Min at 0)
    score = max(0, min(score, 100))
    normalized_score = score / 100.0

    # Determine Decision Tier
    if normalized_score >= 0.8:
        decision = "HOT"
        confidence = 0.95
    elif normalized_score >= 0.6:
        decision = "QUALIFIED"
        confidence = 0.85
    elif normalized_score >= 0.35:
        decision = "WARM"
        confidence = 0.70
    else:
        decision = "NURTURE"
        confidence = 0.60

    # Special Override: If explicitly "No Budget" AND "Just Browsing", force Nurture
    if "No Budget" in message and "Just Browsing" in message:
        decision = "NURTURE"
        normalized_score = 0.1
        confidence = 0.9

    return {
        "lead_id": payload.get("lead_id"),
        "decision": decision,
        "score": normalized_score,
        "confidence": confidence,
        "details": {
            "name": name,
            "company": company,
            "message_snippet": message[:100] if message else ""
        },
        "signals": {
            "email": {"type": "intro_meeting"},
            "company": {"size": "Unknown", "industry": "Technology"},
            "message": {"intent": "interest"}
        }
    }

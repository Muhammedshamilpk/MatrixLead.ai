# qualification_graph.py

def run_qualification(payload: dict):
    """
    Simple AI-style logic to qualify leads automatically.
    """

    name = payload.get("name")
    company = payload.get("company")
    message = payload.get("message")

    score = 0

    # Scoring rules
    if name:
        score += 10
    if company:
        score += 20
    if message:
        score += min(len(message), 200) / 4  # message influences score

    score = min(score, 100)

    # Decide qualification
    decision = "QUALIFIED" if score >= 40 else "NOT_QUALIFIED"

    return {
        "lead_id": payload.get("lead_id"),
        "decision": decision,
        "score": score,
        "details": {
            "name": name,
            "company": company,
            "message": message
        }
    }

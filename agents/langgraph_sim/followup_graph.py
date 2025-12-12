# followup_graph.py

def run_followup(payload: dict):
    """
    Creates auto email text when a lead is qualified.
    """

    name = payload.get("name") or "there"
    company = payload.get("company") or "your company"

    email_text = f"""
Hello {name},

Thank you for reaching out! Our AI system analyzed your details
regarding {company} and it looks like a strong fit.

Our team will contact you soon with more information.

Regards,
MatrixLead AI Agent
"""

    return {
        "lead_id": payload.get("lead_id"),
        "email_text": email_text
    }

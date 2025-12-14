from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..crud.lead_crud import update_lead_status, create_log
from ..models.lead import Lead
import json
import os
import httpx

router = APIRouter(prefix="/api/internal")


@router.post("/agent_result")
def agent_result(payload: dict, db: Session = Depends(get_db)):
    lead_id = payload.get("lead_id")
    decision = payload.get("decision")
    score = payload.get("score", 0.0)
    signals = payload.get("signals", {})
    confidence = payload.get("confidence", 0.0)
    risk_flags = payload.get("risk_flags", [])

    AGENTS_URL = os.getenv("AGENTS_URL", "http://agents:8010")

    print(f"🔔 RESULT RECEIVED | ID: {lead_id} | DECISION: {decision} | SCORE: {score}")

    # Update lead with confidence and risk_flags
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if lead:
        lead.confidence = confidence
        lead.risk_flags = risk_flags
        db.commit()

    # Handle different qualification tiers with AUTOMATIC email sending
    if decision in ["HOT", "QUALIFIED", "WARM"]:
        print(f"⚡ AUTOMATIC TRIGGER: Sending email for {decision} lead...")
        # High and medium priority leads - send email automatically
        update_lead_status(db, lead_id, decision, score)
        
        # Extract detailed information from signals
        email_data = signals.get("email", {})
        company_data = signals.get("company", {})
        name_data = signals.get("name", {})
        message_data = signals.get("message", {})
        
        # TRIGGER AUTOMATIC EMAIL SENDING
        try:
            print(f"   -> Calling Agents Service: {AGENTS_URL}/run/sales_followup")
            response = httpx.post(
                f"{AGENTS_URL}/run/sales_followup",
                json={
                    "lead_id": lead_id,
                    "name": lead.name if lead else None,
                    "email": lead.email if lead else None,
                    "company": lead.company if lead else None,
                    "score": score,
                    "decision": decision,
                    "confidence": confidence,
                    # Additional context for personalization
                    "email_type": email_data.get("type"),
                    "company_size": company_data.get("size"),
                    "company_industry": company_data.get("industry"),
                    "message_intent": message_data.get("intent"),
                },
                timeout=10
            )
            print(f"   -> Response Code: {response.status_code}")
            
            # Log email sending result
            if response.status_code == 200:
                result = response.json()
                create_log(db, lead_id, "auto_email_sent", {
                    "status": result.get("status"),
                    "decision": decision,
                    "score": score,
                    "sent_by": "agent_automatic"
                })
            
        except Exception as e:
            print(f"Failed to trigger sales agent: {e}")
            create_log(db, lead_id, "auto_email_failed", {
                "error": str(e),
                "decision": decision
            })

    elif decision == "NURTURE":
        # Medium-priority leads - add to nurture campaign (no immediate email)
        update_lead_status(db, lead_id, "NURTURE", score)
        create_log(db, lead_id, "nurture_campaign_added", {
            "score": score,
            "confidence": confidence,
            "risk_flags": risk_flags
        })

    elif decision == "REVIEW":
        # Needs manual review
        update_lead_status(db, lead_id, "REVIEW", score)
        create_log(db, lead_id, "manual_review_required", {
            "score": score,
            "confidence": confidence,
            "risk_flags": risk_flags
        })
    else:
        # NOT_QUALIFIED
        update_lead_status(db, lead_id, "NOT_QUALIFIED", score)

    create_log(
        db,
        lead_id,
        "agent_result",
        {
            "decision": decision, 
            "score": score, 
            "confidence": confidence,
            "risk_flags": risk_flags,
            "signals": signals
        },
    )

    return {"status": "ok"}


@router.post("/trigger_qualification/{lead_id}")
def trigger_qualification(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return {"error": "not found"}

    # -----------------------------
    # NORMALIZE lead.data
    # -----------------------------
    raw_data = lead.data

    # A: already dict
    if isinstance(raw_data, dict):
        pass

    # B: JSON string
    elif isinstance(raw_data, str):
        try:
            raw_data = json.loads(raw_data)
            if not isinstance(raw_data, dict):
                raw_data = {}
        except Exception:
            raw_data = {}

    # C: anything else (int, list, None, bool)
    else:
        raw_data = {}

    # Safety: ensure raw_data is always dict
    if not isinstance(raw_data, dict):
        raw_data = {}

    # -----------------------------
    # Build payload
    # -----------------------------
    payload = {
        "lead_id": lead.id,
        "email": lead.email,
        "phone": lead.phone,
        "name": lead.name,
        "company": lead.company,
        "message": raw_data.get("message"),   # NOW ALWAYS SAFE
    }

    # -----------------------------
    # Send to agents service
    # -----------------------------
    AGENTS_URL = os.getenv("AGENTS_URL", "http://agents:8010")

    try:
        httpx.post(
            f"{AGENTS_URL}/run/qualification",
            json=payload,
            timeout=60,
        )
    except Exception as e:
        print(f"⚠️ Failed to trigger agent qualification: {e}")
        # Build a safe signals object for the log
        create_log(db, lead_id, "qualification_failed", {"error": str(e)})
        return {"status": "triggered_but_failed", "error": str(e)}

    create_log(db, lead_id, "qualification_triggered", payload)

    return {"status": "triggered"}

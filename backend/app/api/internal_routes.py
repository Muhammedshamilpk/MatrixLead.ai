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
    details = payload.get("details")

    AGENTS_URL = os.getenv("AGENTS_URL", "http://agents:8010")

    if decision in ["QUALIFIED", "CONTACT"]:
        update_lead_status(db, lead_id, "QUALIFIED", score)
        
        # TRIGGER SALES AGENT
        try:
             httpx.post(
                f"{AGENTS_URL}/run/sales_followup",
                json={
                    "lead_id": lead_id,
                    "name": details.get("name", {}).get("name") if details else None, 
                    "company": details.get("company", {}).get("company") if details else None,
                    "score": score,
                    "decision": decision
                },
                timeout=5
            )
        except Exception as e:
            print(f"Failed to trigger sales agent: {e}")

    elif decision == "IN_PROGRESS":
        update_lead_status(db, lead_id, "IN_PROGRESS", score)
    else:
        update_lead_status(db, lead_id, "NOT_QUALIFIED", score)

    create_log(
        db,
        lead_id,
        "agent_result",
        {"decision": decision, "score": score, "details": details},
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

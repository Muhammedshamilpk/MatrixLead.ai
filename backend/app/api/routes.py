from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from ..schemas.lead_schema import LeadCreate, LeadOut, LogOut
from ..crud.lead_crud import create_lead, list_leads, get_lead_logs, create_log
from ..core.database import get_db
from ..models.lead import Lead
import httpx
import os

router = APIRouter(prefix="/api")

@router.post("/leads", response_model=LeadOut)
def create_new_lead(lead: LeadCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    
    new_lead = create_lead(db, lead)
    
    # Trigger Qualification
    from app.api.internal_routes import trigger_qualification
    background_tasks.add_task(trigger_qualification, new_lead.id, db)
    
    return new_lead

@router.get("/leads", response_model=list[LeadOut])
def get_all_leads(db: Session = Depends(get_db)):
    return list_leads(db)

@router.get("/leads/{lead_id}/logs", response_model=list[LogOut])
def get_lead_logs_endpoint(lead_id: int, db: Session = Depends(get_db)):
    return get_lead_logs(db, lead_id)

@router.post("/leads/{lead_id}/send-email")
def send_email_to_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    Manually send email to a specific lead from the Email UI.
    """
    # Get lead from database
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if not lead.email:
        raise HTTPException(status_code=400, detail="Lead has no email address")
    
    # Get agents service URL
    AGENTS_URL = os.getenv("AGENTS_URL", "http://agents:8010")
    
    try:
        # Call sales agent to send email
        response = httpx.post(
            f"{AGENTS_URL}/run/sales_followup",
            json={
                "lead_id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "company": lead.company,
                "score": lead.score or 0.75,
                "decision": lead.status or "QUALIFIED",
                "confidence": lead.confidence or 0.8,
            },
            timeout=15
        )
        
        result = response.json()
        
        if result.get("status") == "sent":
            # Log email sending success
            create_log(db, lead_id, "manual_email_sent", {
                "status": "sent",
                "to": lead.email,
                "decision": lead.status,
                "sent_from": "email_ui"
            })
            
            return {
                "success": True,
                "message": f"Email sent to {lead.email}",
                "result": result
            }
        else:
            # Handle failure
            error_msg = result.get("error", "Unknown error")
            create_log(db, lead_id, "manual_email_failed", {
                "error": error_msg,
                "to": lead.email,
                "sent_from": "email_ui"
            })
            
            return {
                "success": False,
                "message": f"Failed to send email: {error_msg}. Check SMTP configuration in agents/.env",
                "result": result
            }
        
    except httpx.HTTPError as e:
        create_log(db, lead_id, "manual_email_failed", {
            "error": str(e),
            "to": lead.email,
            "sent_from": "email_ui"
        })
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


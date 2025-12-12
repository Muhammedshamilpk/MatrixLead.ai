from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..schemas.lead_schema import LeadCreate, LeadOut, LogOut
from ..crud.lead_crud import create_lead, list_leads, get_lead_logs
from ..core.database import get_db

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


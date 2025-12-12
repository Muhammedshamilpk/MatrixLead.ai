# from sqlalchemy.orm import Session
# from ..models.lead import Lead
# from ..schemas.lead_schema import LeadCreate

# def create_lead(db: Session, lead_in: LeadCreate):
#     lead = Lead(
#         name=lead_in.name,
#         email=lead_in.email,
#         phone=lead_in.phone,
#         company=lead_in.company,
#         budget=lead_in.budget,
#         source=lead_in.source,
#         data=lead_in.data
#     )
#     db.add(lead)
#     db.commit()
#     db.refresh(lead)
#     return lead

# def list_leads(db: Session):
#     return db.query(Lead).all()


from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.models.log import Log
from app.schemas.lead_schema import LeadCreate


# -----------------------------
# CREATE NEW LEAD
# -----------------------------
def create_lead(db: Session, lead: LeadCreate):
    new_lead = Lead(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        budget=lead.budget,
        source=lead.source,
        data=lead.data
    )
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead


# -----------------------------
# LIST ALL LEADS
# -----------------------------
def list_leads(db: Session):
    return db.query(Lead).all()


# -----------------------------
# UPDATE LEAD STATUS + SCORE
# -----------------------------
def update_lead_status(db: Session, lead_id: int, status: str, score: float):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return None
    
    lead.status = status
    lead.score = score
    db.commit()
    return lead


# -----------------------------
# CREATE LOG ENTRY
# -----------------------------
def create_log(db: Session, lead_id: int, action: str, details: dict):
    log = Log(
        lead_id=lead_id,
        action=action,
        details=details
    )
    db.add(log)
    db.commit()
    return log


# -----------------------------
# GET LEAD LOGS
# -----------------------------
def get_lead_logs(db: Session, lead_id: int):
    return db.query(Log).filter(Log.lead_id == lead_id).order_by(Log.timestamp.asc()).all()

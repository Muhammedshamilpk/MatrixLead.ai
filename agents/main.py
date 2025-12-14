from fastapi import FastAPI
from pydantic import BaseModel

from langgraph_sim.qualification_graph import run_qualification
from langgraph_sim.followup_graph import run_followup

app = FastAPI(title="MatrixLead Agent Service")

class LeadPayload(BaseModel):
    lead_id: int
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    message: str | None = None
    
    # Qualification Data
    decision: str | None = None
    score: float | None = None
    confidence: float | None = None
    
    # Context Data
    email_type: str | None = None
    company_size: str | None = None
    company_industry: str | None = None
    message_intent: str | None = None

@app.get("/")
def health():
    return {"message": "Agent service running"}

@app.post("/run/qualification")
def qualification_route(payload: LeadPayload):
    result = run_qualification(payload.dict())
    return {"status": "ok", "result": result}

@app.post("/run/sales_followup")
async def sales_route(payload: LeadPayload):
    from sales_agent import generate_followup, send_communication
    
    # 1. Generate the personalized email
    msg_payload = await generate_followup(payload.dict())
    
    # 2. Automatically SEND the email
    result = await send_communication(msg_payload)
    
    return {"status": "ok", "result": result}

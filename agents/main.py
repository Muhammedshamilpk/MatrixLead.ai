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

@app.get("/")
def health():
    return {"message": "Agent service running"}

@app.post("/run/qualification")
def qualification_route(payload: LeadPayload):
    result = run_qualification(payload.dict())
    return {"status": "ok", "result": result}

@app.post("/run/sales_followup")
def sales_route(payload: LeadPayload):
    result = run_followup(payload.dict())
    return {"status": "ok", "result": result}

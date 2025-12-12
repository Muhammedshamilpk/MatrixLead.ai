# agents/agent_runner.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx, os, asyncio
from sales_agent import generate_followup, send_communication

app = FastAPI(title="Agents Runner")

# MCP TOOL ENDPOINTS (all inside one container)
MCP = "http://mcp_service:9000/tools"

EMAIL_URL = f"{MCP}/email_reputation"
PHONE_URL = f"{MCP}/phone_check"
NAME_URL = f"{MCP}/name_check"
COMPANY_URL = f"{MCP}/company_enrich"
MESSAGE_URL = f"{MCP}/intent"

# Aggregation tool
AGG_URL = f"{MCP}/aggregate"

# Backend callback
BACKEND_URL = "http://backend:8000"



class LeadIn(BaseModel):
    lead_id: int
    email: str | None = None
    phone: str | None = None
    name: str | None = None
    company: str | None = None
    message: str | None = None


def safe_json(response):
    """Return {} on error."""
    try:
        return response.json()
    except:
        return {}


@app.post("/run/qualification")
async def run_qualification(payload: LeadIn):

    async with httpx.AsyncClient(timeout=40) as client:

        tasks = [
            client.post(EMAIL_URL, json={"email": payload.email}),
            client.post(PHONE_URL, json={"phone": payload.phone}),
            client.post(NAME_URL, json={"name": payload.name}),
            client.post(COMPANY_URL, json={"company": payload.company}),
            client.post(MESSAGE_URL, json={"message": payload.message}),
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert to JSON results
        email_res, phone_res, name_res, company_res, message_res = [
            safe_json(r) if not isinstance(r, Exception) else {}
            for r in responses
        ]

        # DEFAULT SCORES → prevents aggregator crash
        email_res.setdefault("score", 0.5)
        phone_res.setdefault("score", 0.5)
        name_res.setdefault("score", 0.5)
        company_res.setdefault("score", 0.5)
        message_res.setdefault("score", 0.5)

        # BUILD correct aggregator payload
        agg_payload = {
            "lead_id": payload.lead_id,
            "email": email_res,
            "phone": phone_res,
            "name": name_res,
            "company": company_res,
            "message": message_res
        }

        # CALL AGGREGATOR
        agg = (await client.post(AGG_URL, json=agg_payload)).json()

        # SEND RESULT TO BACKEND
        await client.post(f"{BACKEND_URL}/api/internal/agent_result", json={
            "lead_id": payload.lead_id,
            "decision": agg["decision"],
            "score": agg["total_score"],  # FIXED
            "signals": agg_payload
        })


        return {
            "status": "OK",
            "decision": agg["decision"],
            "total_score": agg["total_score"],
            "signals": agg_payload
        }


@app.post("/run/sales_followup")
async def run_sales_followup(payload: dict):
    """
    payload expected:
    {
        "lead_id": 123,
        "name": "...",
        "company": "...",
        "score": 85,
        "decision": "CONTACT"
    }
    """
    # 1. Generate Content
    message = await generate_followup(payload)
    
    # 2. Send (if message generated)
    result = await send_communication(message)
    
    return {
        "lead_id": payload.get("lead_id"),
        "action_taken": result
    }


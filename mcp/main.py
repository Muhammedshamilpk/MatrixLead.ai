from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Import routers from submodules
from company_tool.main import router as company_router
from email_tool.main import router as email_router
from phone_tool.main import router as phone_router
from name_tool.main import router as name_router
from message_tool.main import router as message_router
from aggregator.main import router as aggregator_router

load_dotenv()

app = FastAPI(title="Unified MCP Service")

# Include routers
app.include_router(company_router)
app.include_router(email_router)
app.include_router(phone_router)
app.include_router(name_router)
app.include_router(message_router)
app.include_router(aggregator_router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Unified MCP Service"}

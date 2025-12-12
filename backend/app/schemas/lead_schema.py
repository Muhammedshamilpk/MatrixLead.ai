from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class LeadCreate(BaseModel):
    name: str
    email: str
    phone: str
    company: Optional[str] = None
    budget: Optional[str] = None
    source: Optional[str] = None
    data: Optional[Any] = None


class LeadOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    company: Optional[str]
    budget: Optional[str]
    source: Optional[str]
    data: Optional[Any]

    messages: Optional[list[dict]] = []
    lastMessage: Optional[str] = None

    status: str
    score: float
    confidence: Optional[float]
    risk_flags: Optional[Any]
    enriched: Optional[bool]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class LogOut(BaseModel):
    id: int
    lead_id: int
    action: str
    details: Optional[Any]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

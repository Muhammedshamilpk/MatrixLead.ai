from sqlalchemy import (
    Column, Integer, String, DateTime, JSON, Float, Boolean
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    # Basic lead info
    name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(100))
    company = Column(String(200))
    budget = Column(String(100), nullable=True)
    source = Column(String(100), nullable=True)

    # Data stored from form/website
    data = Column(JSON)

    # AI / Agent status tracking
    messages = Column(JSON, default=[])         # Chat history
    status = Column(String(50), default="NEW")  # NEW / QUALIFIED / IN_PROGRESS / NOT_QUALIFIED
    score = Column(Float, default=0.0)          # final aggregated score 0..1
    confidence = Column(Float, default=0.0)     # AI confidence score
    risk_flags = Column(JSON, nullable=True)    # e.g. {"email":"disposable","phone":"invalid"}
    enriched = Column(Boolean, default=False)   # enrichment completed or not

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to logs
    logs = relationship("Log", back_populates="lead")

    @property
    def lastMessage(self):
        if self.messages and isinstance(self.messages, list) and len(self.messages) > 0:
            last = self.messages[-1]
            if isinstance(last, dict):
                return last.get("text")
        return None

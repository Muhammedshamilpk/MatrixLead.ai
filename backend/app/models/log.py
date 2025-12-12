from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)

    action = Column(String(100), nullable=False)
    details = Column(JSON, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="logs")

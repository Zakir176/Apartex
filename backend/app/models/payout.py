from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Date
from datetime import datetime
from app.database import Base

class Payout(Base):
    __tablename__ = "payouts"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending")  # pending, processed, completed
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
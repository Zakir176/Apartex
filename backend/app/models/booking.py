from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Date
from datetime import datetime
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled, completed
    guests = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
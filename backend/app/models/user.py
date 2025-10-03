from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    role = Column(String, default="renter")
    is_active = Column(Boolean, default=True)
    
    # Loyalty system fields
    total_bookings = Column(Integer, default=0)
    loyalty_points = Column(Integer, default=0)
    loyalty_tier = Column(String, default="bronze")  # bronze, silver, gold
    has_pending_reward = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Fix relationships - use strings to avoid circular imports
    bookings = relationship("Booking", back_populates="user")
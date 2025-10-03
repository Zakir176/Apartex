from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from datetime import datetime
from app.database import Base

class LoyaltyReward(Base):
    __tablename__ = "loyalty_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_type = Column(String(50), nullable=False)  # 'free_night', 'percentage_discount'
    reward_value = Column(Numeric(10, 2))  # 10.00 for 10% discount, or NULL for free night
    status = Column(String(20), default="available")  # available, used, expired
    earned_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # For tracking which booking earned this reward
    earned_from_booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
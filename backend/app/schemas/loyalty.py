from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class RewardType(str, Enum):
    FREE_NIGHT = "free_night"
    PERCENTAGE_DISCOUNT = "percentage_discount"

class RewardStatus(str, Enum):
    AVAILABLE = "available"
    USED = "used"
    EXPIRED = "expired"

class LoyaltyTier(str, Enum):
    BRONZE = "bronze"    # 0-2 bookings
    SILVER = "silver"    # 3-9 bookings  
    GOLD = "gold"        # 10+ bookings

class LoyaltyStatus(BaseModel):
    user_id: int
    total_bookings: int
    loyalty_points: int
    loyalty_tier: LoyaltyTier
    has_pending_reward: bool
    next_reward_at: int  # Bookings needed for next reward
    rewards_available: int

    class Config:
        from_attributes = True

class LoyaltyRewardBase(BaseModel):
    reward_type: RewardType
    reward_value: Optional[float] = None  # For percentage discounts

class LoyaltyRewardCreate(LoyaltyRewardBase):
    user_id: int

class LoyaltyRewardRead(LoyaltyRewardBase):
    id: int
    user_id: int
    status: RewardStatus
    earned_at: datetime
    used_at: Optional[datetime]
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class RewardRedemption(BaseModel):
    reward_id: int
    booking_id: int
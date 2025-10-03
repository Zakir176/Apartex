from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user import User
from app.models.booking import Booking
from app.models.loyalty import LoyaltyReward
from app.schemas.loyalty import LoyaltyTier, RewardType

class LoyaltyService:
    
    @staticmethod
    def calculate_loyalty_tier(total_bookings: int) -> LoyaltyTier:
        """Calculate user's loyalty tier based on total bookings."""
        if total_bookings >= 10:
            return LoyaltyTier.GOLD
        elif total_bookings >= 3:
            return LoyaltyTier.SILVER
        else:
            return LoyaltyTier.BRONZE
    
    @staticmethod
    def calculate_points_for_booking(booking_total: float, user_tier: LoyaltyTier) -> int:
        """Calculate loyalty points earned for a booking."""
        base_points = int(booking_total)  # 1 point per currency unit
        
        # Tier multipliers
        multipliers = {
            LoyaltyTier.BRONZE: 1.0,
            LoyaltyTier.SILVER: 1.5, 
            LoyaltyTier.GOLD: 2.0
        }
        
        return int(base_points * multipliers[user_tier])
    
    @staticmethod
    def check_reward_eligibility(total_bookings: int) -> bool:
        """Check if user is eligible for a reward (every 3 bookings)."""
        return total_bookings > 0 and total_bookings % 3 == 0
    
    @staticmethod
    def grant_reward(user_id: int, booking_id: int, db: Session):
        """Grant a reward to user for reaching booking milestone."""
        # Determine reward type (alternate between discount and free night)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Alternate reward types
        if user.total_bookings % 6 == 0:  # Every 6 bookings = free night
            reward_type = RewardType.FREE_NIGHT
            reward_value = None
        else:  # Every 3 bookings = discount
            reward_type = RewardType.PERCENTAGE_DISCOUNT
            reward_value = 10.0  # 10% discount
        
        # Create reward
        reward = LoyaltyReward(
            user_id=user_id,
            reward_type=reward_type,
            reward_value=reward_value,
            earned_from_booking_id=booking_id,
            expires_at=datetime.utcnow() + timedelta(days=365)  # 1 year expiry
        )
        
        db.add(reward)
        user.has_pending_reward = True
        db.commit()
        db.refresh(reward)
        
        return reward
    
    @staticmethod
    def process_booking_completion(booking: Booking, db: Session):
        """Process loyalty points and rewards when a booking is completed."""
        user = db.query(User).filter(User.id == booking.user_id).first()
        if not user:
            return
        
        # Update user booking count
        user.total_bookings += 1
        
        # Calculate and award loyalty points
        points_earned = LoyaltyService.calculate_points_for_booking(
            float(booking.total_price), 
            user.loyalty_tier
        )
        user.loyalty_points += points_earned
        booking.earned_loyalty_points = points_earned
        
        # Update loyalty tier
        user.loyalty_tier = LoyaltyService.calculate_loyalty_tier(user.total_bookings)
        
        # Check for reward eligibility
        if LoyaltyService.check_reward_eligibility(user.total_bookings):
            LoyaltyService.grant_reward(user.id, booking.id, db)
        else:
            user.has_pending_reward = False
        
        db.commit()
    
    @staticmethod
    def get_loyalty_status(user_id: int, db: Session):
        """Get comprehensive loyalty status for a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Count available rewards
        available_rewards = db.query(LoyaltyReward).filter(
            LoyaltyReward.user_id == user_id,
            LoyaltyReward.status == "available"
        ).count()
        
        # Calculate next reward
        next_reward_at = 3 - (user.total_bookings % 3)
        if next_reward_at == 3:
            next_reward_at = 0  # User is exactly at a reward milestone
        
        return {
            "user_id": user.id,
            "total_bookings": user.total_bookings,
            "loyalty_points": user.loyalty_points,
            "loyalty_tier": user.loyalty_tier,
            "has_pending_reward": user.has_pending_reward,
            "next_reward_at": next_reward_at,
            "rewards_available": available_rewards
        }
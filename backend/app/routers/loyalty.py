from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.loyalty import LoyaltyReward
from app.models.user import User
from app.models.booking import Booking
from datetime import datetime
from app.schemas.loyalty import (
    LoyaltyStatus, LoyaltyRewardRead, RewardRedemption,
    RewardType, RewardStatus
)
from app.services.loyalty_service import LoyaltyService
from decimal import Decimal
import logging

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@router.get("/users/{user_id}/status", response_model=LoyaltyStatus)
def get_loyalty_status(user_id: int, db: Session = Depends(get_db)):
    """Get loyalty status and rewards for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    status = LoyaltyService.get_loyalty_status(user_id, db)
    return status

@router.get("/users/{user_id}/rewards", response_model=List[LoyaltyRewardRead])
def get_user_rewards(user_id: int, db: Session = Depends(get_db)):
    """Get all rewards for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    rewards = db.query(LoyaltyReward).filter(
        LoyaltyReward.user_id == user_id
    ).order_by(LoyaltyReward.earned_at.desc()).all()
    
    return rewards

@router.post("/rewards/redeem")
def redeem_reward(redemption: RewardRedemption, db: Session = Depends(get_db)):
    """Redeem a reward for a booking."""
    logger.info("🚀 Starting reward redemption...")

    # Check if reward exists and is available
    reward = db.query(LoyaltyReward).filter(
        LoyaltyReward.id == redemption.reward_id,
        LoyaltyReward.status == "available"
    ).first()
    
    if not reward:
        raise HTTPException(status_code=404, detail="Reward not found or already used")
    
    logger.info(f"✅ Reward found: {reward.reward_type} {reward.reward_value}%")

    # Check if booking exists
    booking = db.query(Booking).filter(Booking.id == redemption.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    logger.info(f"✅ Booking found: ${booking.total_price}")

    # Check if reward belongs to booking user
    if reward.user_id != booking.user_id:
        raise HTTPException(status_code=400, detail="Reward does not belong to booking user")
    
    # Use Decimal for financial calculations
    original_price = Decimal(str(booking.total_price))
    discount_percent = Decimal(str(reward.reward_value))
    
    logger.info(f"💰 Original price: ${original_price}")
    logger.info(f"🎯 Discount: {discount_percent}%")
    
    # Calculate new price
    new_price = original_price * (1 - discount_percent / Decimal('100'))
    
    logger.info(f"💰 New price: ${new_price}")
    
    # Apply the discount to the booking
    booking.total_price = new_price
    booking.used_reward_id = reward.id
    
    # Mark the reward as used
    reward.status = "used"
    reward.used_at = datetime.utcnow()
    
    # Update user's pending reward status
    user = db.query(User).filter(User.id == reward.user_id).first()
    if user:
        user.has_pending_reward = False
    
    try:
        db.commit()
        logger.info("✅ Reward applied successfully!")
    except Exception as e:
        db.rollback()  # Rollback in case of error
        logger.error(f"Error applying reward: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return {
        "message": "Reward applied successfully!",
        "booking_id": booking.id,
        "original_price": float(original_price),
        "new_total_price": float(new_price),
        "savings": float(original_price - new_price)
    }

@router.put("/bookings/{booking_id}/complete")
def complete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Mark a booking as completed and process loyalty rewards."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == "completed":
        raise HTTPException(status_code=400, detail="Booking already completed")
    
    # Update booking status to 'completed'
    booking.status = "completed"
    
    # Process loyalty rewards
    LoyaltyService.process_booking_completion(booking, db)
    
    # Refresh booking data after processing
    db.refresh(booking)
    
    # Get the user separately to avoid relationship issues
    user = db.query(User).filter(User.id == booking.user_id).first()
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback in case of error
        logger.error(f"Error completing booking: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return {
        "message": "Booking marked as completed",
        "booking_id": booking.id,
        "points_earned": booking.earned_loyalty_points,
        "user_total_bookings": user.total_bookings if user else 0
    }

@router.get("/tiers")
def get_loyalty_tiers():
    """Get information about loyalty tiers and benefits."""
    return {
        "tiers": [
            {
                "name": "bronze",
                "min_bookings": 0,
                "max_bookings": 2,
                "point_multiplier": 1.0,
                "benefits": ["Basic rewards"]
            },
            {
                "name": "silver", 
                "min_bookings": 3,
                "max_bookings": 9,
                "point_multiplier": 1.5,
                "benefits": ["50% more points", "Rewards every 3 bookings"]
            },
            {
                "name": "gold",
                "min_bookings": 10,
                "point_multiplier": 2.0,
                "benefits": ["Double points", "Priority support", "Exclusive deals"]
            }
        ],
        "rewards": [
            {
                "frequency": "Every 3 bookings",
                "types": ["10% discount", "Free night (every 6 bookings)"]
            }
        ]
    }

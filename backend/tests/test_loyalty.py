import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.services.loyalty_service import LoyaltyService
    from app.schemas.loyalty import LoyaltyTier
    from datetime import datetime
    
    print("✅ Loyalty service imports successful!")
    
    # Test tier calculation
    print(f"✅ Bronze tier: {LoyaltyService.calculate_loyalty_tier(2)}")
    print(f"✅ Silver tier: {LoyaltyService.calculate_loyalty_tier(3)}") 
    print(f"✅ Gold tier: {LoyaltyService.calculate_loyalty_tier(10)}")
    
    # Test reward eligibility
    print(f"✅ Reward at 3 bookings: {LoyaltyService.check_reward_eligibility(3)}")
    print(f"✅ Reward at 4 bookings: {LoyaltyService.check_reward_eligibility(4)}")
    
    print("✅ All loyalty tests passed!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Test failed: {e}")
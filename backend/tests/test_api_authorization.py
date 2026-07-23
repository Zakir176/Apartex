import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Booking, Property, LoyaltyReward
from app.core.security import create_access_token

client = TestClient(app)

def test_secured_api_authorization():
    # Make sure all tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Create user A (renter)
        email_a = f"usera_{int(datetime.now().timestamp())}@example.com"
        user_a = User(
            email=email_a,
            hashed_password="hashed_password",
            full_name="User A",
            role="renter",
            is_active=True
        )
        db.add(user_a)
        
        # Create user B (renter)
        email_b = f"userb_{int(datetime.now().timestamp())}@example.com"
        user_b = User(
            email=email_b,
            hashed_password="hashed_password",
            full_name="User B",
            role="renter",
            is_active=True
        )
        db.add(user_b)
        db.commit()
        
        # Access tokens
        token_a = create_access_token({"sub": user_a.email})
        token_b = create_access_token({"sub": user_b.email})
        
        # -------------------------------------------------------------
        # 1. Test Bookings: /api/bookings/user/{user_id}/bookings
        # -------------------------------------------------------------
        
        # Unauthenticated: should return 401
        res = client.get(f"/api/bookings/user/{user_a.id}/bookings")
        assert res.status_code == 401
        
        # Authenticated as User A requesting A's bookings: should return 200
        headers_a = {"Authorization": f"Bearer {token_a}"}
        res = client.get(f"/api/bookings/user/{user_a.id}/bookings", headers=headers_a)
        assert res.status_code == 200
        
        # Authenticated as User B requesting A's bookings: should return 403
        headers_b = {"Authorization": f"Bearer {token_b}"}
        res = client.get(f"/api/bookings/user/{user_a.id}/bookings", headers=headers_b)
        assert res.status_code == 403
        
        # -------------------------------------------------------------
        # 2. Test Loyalty Status: /api/loyalty/users/{user_id}/status
        # -------------------------------------------------------------
        
        # Unauthenticated: should return 401
        res = client.get(f"/api/loyalty/users/{user_a.id}/status")
        assert res.status_code == 401
        
        # Authenticated as User A requesting A's status: should return 200
        res = client.get(f"/api/loyalty/users/{user_a.id}/status", headers=headers_a)
        assert res.status_code == 200
        
        # Authenticated as User B requesting A's status: should return 403
        res = client.get(f"/api/loyalty/users/{user_a.id}/status", headers=headers_b)
        assert res.status_code == 403
        
        # -------------------------------------------------------------
        # 3. Test Loyalty Rewards: /api/loyalty/users/{user_id}/rewards
        # -------------------------------------------------------------
        
        # Unauthenticated: should return 401
        res = client.get(f"/api/loyalty/users/{user_a.id}/rewards")
        assert res.status_code == 401
        
        # Authenticated as User A requesting A's rewards: should return 200
        res = client.get(f"/api/loyalty/users/{user_a.id}/rewards", headers=headers_a)
        assert res.status_code == 200
        
        # Authenticated as User B requesting A's rewards: should return 403
        res = client.get(f"/api/loyalty/users/{user_a.id}/rewards", headers=headers_b)
        assert res.status_code == 403
        
        # -------------------------------------------------------------
        # 4. Test Loyalty Reward Redemption: /api/loyalty/rewards/redeem
        # -------------------------------------------------------------
        
        # Create a test apartment owned by host ID 1
        apartment = Property(
            title="Authorization Test Villa",
            address="123 Auth St",
            city="Lusaka",
            price_per_night=100.0,
            capacity=2,
            bedrooms=1,
            bathrooms=1,
            owner_id=1
        )
        db.add(apartment)
        db.flush()
        
        # Create booking for user A
        booking_a = Booking(
            user_id=user_a.id,
            property_id=apartment.id,
            check_in=datetime.now().date(),
            check_out=(datetime.now() + timedelta(days=2)).date(),
            total_price=200.0,
            status="confirmed"
        )

        db.add(booking_a)
        db.flush()
        
        # Create reward for user A
        reward_a = LoyaltyReward(
            user_id=user_a.id,
            reward_type="percentage_discount",
            reward_value=10.0,
            earned_from_booking_id=booking_a.id,
            expires_at=datetime.utcnow() + timedelta(days=365),
            status="available"
        )
        db.add(reward_a)
        db.commit()
        db.refresh(reward_a)
        db.refresh(booking_a)
        
        # Unauthenticated: should return 401
        res = client.post("/api/loyalty/rewards/redeem", json={
            "reward_id": reward_a.id,
            "booking_id": booking_a.id
        })
        assert res.status_code == 401
        
        # Authenticated as User B (not the reward owner): should return 403
        res = client.post("/api/loyalty/rewards/redeem", json={
            "reward_id": reward_a.id,
            "booking_id": booking_a.id
        }, headers=headers_b)
        assert res.status_code == 403
        
        # Authenticated as User A (reward owner): should return 200 (Success)
        res = client.post("/api/loyalty/rewards/redeem", json={
            "reward_id": reward_a.id,
            "booking_id": booking_a.id
        }, headers=headers_a)
        assert res.status_code == 200
        
        print("🚀 API Authorization verification SUCCESSFUL!")
        
    finally:
        db.close()

def test_apartment_availability_blocked_dates():
    from app.routers.bookings import check_apartment_availability
    from app.models.blocked_date import BlockedDate
    from datetime import date
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Create a test apartment
        apartment = Property(
            title="Availability Test Apt",
            address="456 Availability St",
            city="Lusaka",
            price_per_night=120.0,
            capacity=2,
            bedrooms=1,
            bathrooms=1,
            owner_id=1,
            is_available=True
        )
        db.add(apartment)
        db.flush()
        
        # Block dates: June 15 and June 16
        bd1 = BlockedDate(
            apartment_id=apartment.id,
            blocked_date=date(2026, 6, 15),
            reason="maintenance"
        )
        bd2 = BlockedDate(
            apartment_id=apartment.id,
            blocked_date=date(2026, 6, 16),
            reason="maintenance"
        )
        db.add(bd1)
        db.add(bd2)
        db.commit()
        
        # 1. Check check-in = 14, check-out = 15 (should be available since checkout is 15 exclusive)
        assert check_apartment_availability(apartment.id, date(2026, 6, 14), date(2026, 6, 15), db) is True
        
        # 2. Check check-in = 15, check-out = 16 (should be unavailable)
        assert check_apartment_availability(apartment.id, date(2026, 6, 15), date(2026, 6, 16), db) is False
        
        # 3. Check check-in = 16, check-out = 17 (should be unavailable since 16 is blocked)
        assert check_apartment_availability(apartment.id, date(2026, 6, 16), date(2026, 6, 17), db) is False
        
        # 4. Check check-in = 17, check-out = 18 (should be available)
        assert check_apartment_availability(apartment.id, date(2026, 6, 17), date(2026, 6, 18), db) is True
        
        # 5. Check overlapping range: check-in = 14, check-out = 18 (should be unavailable)
        assert check_apartment_availability(apartment.id, date(2026, 6, 14), date(2026, 6, 18), db) is False
        
        print("🚀 Range-based BlockedDate checks successful!")
    finally:
        db.close()


import sys
import os
from datetime import date, timedelta, datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Booking, LoyaltyReward
from app.core.security import create_access_token

client = TestClient(app)

def test_loyalty_full_flow():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        user1 = User(
            email=f"loyalty1_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Loyalty Renter 1",
            role="renter",
            is_active=True,
            total_bookings=0,
            has_pending_reward=False
        )
        user2 = User(
            email=f"loyalty2_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Loyalty Renter 2",
            role="renter",
            is_active=True
        )
        owner = User(
            email=f"loyalty_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Loyalty Owner",
            role="owner",
            is_active=True
        )
        db.add_all([user1, user2, owner])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        db.refresh(owner)
        
        prop = Property(
            title="Loyalty Villa",
            description="Villa for loyalty testing",
            address="1 Loyalty Way",
            city="Lusaka",
            price_per_night=200.0,
            capacity=2,
            bedrooms=1,
            bathrooms=1,
            owner_id=owner.id,
            property_type="apartment",
            is_available=True
        )
        db.add(prop)
        db.commit()
        db.refresh(prop)
        
        headers1 = {"Authorization": f"Bearer {create_access_token({'sub': user1.email})}"}
        headers2 = {"Authorization": f"Bearer {create_access_token({'sub': user2.email})}"}
        
        # 1. GET /api/loyalty/tiers -> 200 OK
        res = client.get("/api/loyalty/tiers")
        assert res.status_code == 200
        assert "tiers" in res.json()
        assert len(res.json()["tiers"]) == 4
        
        # 2. GET user1 status as user1 -> 200 OK
        res = client.get(f"/api/loyalty/users/{user1.id}/status", headers=headers1)
        assert res.status_code == 200
        assert res.json()["loyalty_tier"] == "bronze"
        
        # 3. GET user1 status as user2 -> 403 Forbidden
        res = client.get(f"/api/loyalty/users/{user1.id}/status", headers=headers2)
        assert res.status_code == 403
        
        # 4. Create confirmed booking for user1
        booking = Booking(
            property_id=prop.id,
            user_id=user1.id,
            check_in=date.today() - timedelta(days=5),
            check_out=date.today() - timedelta(days=3),
            guests=1,
            total_price=400.0,
            status="confirmed"
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        
        # 5. Complete booking via PUT /api/loyalty/bookings/{booking_id}/complete
        res = client.put(f"/api/loyalty/bookings/{booking.id}/complete")
        assert res.status_code == 200
        assert res.json()["booking_id"] == booking.id
        
        # Complete already completed booking -> 400 Bad Request
        res = client.put(f"/api/loyalty/bookings/{booking.id}/complete")
        assert res.status_code == 400
        assert "already completed" in res.json()["detail"]
        
        # 6. Add reward to user1 manually and redeem it
        reward = LoyaltyReward(
            user_id=user1.id,
            reward_type="percentage_discount",
            reward_value=10.0, # 10% off
            status="available"
        )
        db.add(reward)
        db.commit()
        db.refresh(reward)
        
        # Create second booking to apply reward
        booking2 = Booking(
            property_id=prop.id,
            user_id=user1.id,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            guests=1,
            total_price=500.0,
            status="confirmed"
        )
        db.add(booking2)
        db.commit()
        db.refresh(booking2)
        
        # Redeem reward as user2 -> 403 Forbidden
        redemption_payload = {
            "reward_id": reward.id,
            "booking_id": booking2.id
        }
        res = client.post("/api/loyalty/rewards/redeem", json=redemption_payload, headers=headers2)
        assert res.status_code == 403
        
        # Redeem reward as user1 -> 200 OK (500.0 - 10% = 450.0)
        res = client.post("/api/loyalty/rewards/redeem", json=redemption_payload, headers=headers1)
        assert res.status_code == 200
        assert res.json()["new_total_price"] == 450.0
        assert res.json()["savings"] == 50.0
        
        # GET user1 rewards list -> should show reward status "used"
        res = client.get(f"/api/loyalty/users/{user1.id}/rewards", headers=headers1)
        assert res.status_code == 200
        assert len(res.json()) == 1
        assert res.json()[0]["status"] == "used"
        
    finally:
        db.close()

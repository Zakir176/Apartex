import sys
import os
from datetime import date, timedelta, datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Room, Booking
from app.routers.auth_enhanced import create_access_token

client = TestClient(app)

def test_phase2_room_bookings_and_walk_in():
    print("=== Testing Phase 2 Room Bookings & Walk-In Endpoint ===")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"phase2_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Phase2 Host",
            role="owner",
            is_active=True
        )
        renter = User(
            email=f"phase2_renter_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Phase2 Guest",
            role="renter",
            is_active=True
        )
        db.add_all([owner, renter])
        db.commit()
        db.refresh(owner)
        db.refresh(renter)
        
        hotel = Property(
            title="Lusaka Grand Hotel",
            description="Luxury city hotel",
            address="Cairo Road",
            city="Lusaka",
            price_per_night=200.00,
            capacity=20,
            bedrooms=10,
            bathrooms=10,
            owner_id=owner.id,
            property_type="hotel",
            is_available=True
        )
        db.add(hotel)
        db.commit()
        db.refresh(hotel)
        
        deluxe_room = Room(
            property_id=hotel.id,
            room_type="Deluxe Suite",
            description="Deluxe suite with city view",
            price_per_night=150.00,
            capacity=2,
            total_units=2,  # 2 physical rooms
            is_available=True
        )
        db.add(deluxe_room)
        db.commit()
        db.refresh(deluxe_room)
        
        renter_token = create_access_token(data={"sub": renter.email})
        owner_token = create_access_token(data={"sub": owner.email})
        renter_headers = {"Authorization": f"Bearer {renter_token}"}
        owner_headers = {"Authorization": f"Bearer {owner_token}"}
        
        # 1. Regular room booking (POST /api/bookings/)
        check_in = date.today() + timedelta(days=5)
        check_out = date.today() + timedelta(days=7)
        
        booking_payload = {
            "property_id": hotel.id,
            "room_id": deluxe_room.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 2
        }
        res = client.post("/api/bookings/", json=booking_payload, headers=renter_headers)
        assert res.status_code == 201, f"Room booking failed: {res.text}"
        data = res.json()
        assert data["room_id"] == deluxe_room.id
        assert data["total_price"] == 300.00  # 2 nights * $150
        print("✅ Regular room booking succeeded")
        
        # 2. Walk-in room booking (POST /api/bookings/walk-in)
        walk_in_payload = {
            "property_id": hotel.id,
            "room_id": deluxe_room.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 2,
            "is_walk_in": True,
            "payment_method": "cash",
            "walk_in_guest_name": "John Walkin",
            "walk_in_guest_phone": "+260971234567"
        }
        res = client.post("/api/bookings/walk-in", json=walk_in_payload, headers=owner_headers)
        assert res.status_code == 201, f"Walk-in room booking failed: {res.text}"
        data = res.json()
        assert data["room_id"] == deluxe_room.id
        assert data["user_id"] is None
        assert data["walk_in_guest_name"] == "John Walkin"
        print("✅ Walk-in room booking succeeded (2 of 2 units booked)")
        
        # 3. Third room booking should fail (capacity=2 total_units reached)
        res = client.post("/api/bookings/", json=booking_payload, headers=renter_headers)
        assert res.status_code == 400
        assert "Room is not available" in res.json()["detail"]
        print("✅ Overbooking blocked when total_units reached")
        
        # 4. Room availability endpoint (GET /api/bookings/room/{room_id}/availability)
        res = client.get(f"/api/bookings/room/{deluxe_room.id}/availability?check_in={check_in}&check_out={check_out}")
        assert res.status_code == 200
        avail_data = res.json()
        assert avail_data["room_id"] == deluxe_room.id
        assert avail_data["is_available"] is False
        assert avail_data["units_available"] == 0
        assert avail_data["total_units"] == 2
        print("✅ Room availability endpoint verified")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_phase2_room_bookings_and_walk_in()

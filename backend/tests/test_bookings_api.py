import sys
import os
from datetime import date, timedelta, datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Room, Booking
from app.core.security import create_access_token

client = TestClient(app)

def test_bookings_full_lifecycle_and_security():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"b_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Booking Owner",
            role="owner",
            is_active=True
        )
        renter1 = User(
            email=f"b_renter1_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Booking Guest 1",
            role="renter",
            is_active=True,
            loyalty_points=500
        )
        renter2 = User(
            email=f"b_renter2_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Booking Guest 2",
            role="renter",
            is_active=True
        )
        db.add_all([owner, renter1, renter2])
        db.commit()
        db.refresh(owner)
        db.refresh(renter1)
        db.refresh(renter2)
        
        prop = Property(
            title="Kabulonga Luxury Residence",
            description="Luxury residency for booking testing",
            address="15 Kabulonga Rd",
            city="Lusaka",
            price_per_night=250.0,
            capacity=3,
            bedrooms=2,
            bathrooms=2,
            owner_id=owner.id,
            property_type="apartment",
            is_available=True
        )
        db.add(prop)
        db.commit()
        db.refresh(prop)
        
        owner_headers = {"Authorization": f"Bearer {create_access_token({'sub': owner.email})}"}
        renter1_headers = {"Authorization": f"Bearer {create_access_token({'sub': renter1.email})}"}
        renter2_headers = {"Authorization": f"Bearer {create_access_token({'sub': renter2.email})}"}
        
        check_in = date.today() + timedelta(days=15)
        check_out = date.today() + timedelta(days=18)
        
        # 1. Invalid guest capacity (> property capacity) -> 400 Bad Request
        res = client.post("/api/bookings/", json={
            "property_id": prop.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 10
        }, headers=renter1_headers)
        assert res.status_code == 400
        assert "can only accommodate" in res.json()["detail"]
        
        # 2. Valid booking with loyalty points discount (500 pts = $5.00 discount)
        res = client.post("/api/bookings/", json={
            "property_id": prop.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 2,
            "points_applied": 500
        }, headers=renter1_headers)
        assert res.status_code == 201
        b_data = res.json()
        b_id = b_data["id"]
        # 3 nights * $250 - $5 discount = $745.00
        assert b_data["total_price"] == 745.0
        
        # 3. GET /api/bookings/{booking_id} authorization check
        # Owner can view
        res = client.get(f"/api/bookings/{b_id}", headers=owner_headers)
        assert res.status_code == 200
        
        # Renter1 can view
        res = client.get(f"/api/bookings/{b_id}", headers=renter1_headers)
        assert res.status_code == 200
        
        # Unauthorized renter2 cannot view -> 403 Forbidden
        res = client.get(f"/api/bookings/{b_id}", headers=renter2_headers)
        assert res.status_code == 403
        
        # 4. PUT /api/bookings/{booking_id} update booking
        # Unauthorized renter2 cannot update -> 403
        res = client.put(f"/api/bookings/{b_id}", json={"status": "cancelled"}, headers=renter2_headers)
        assert res.status_code == 403
        
        # Renter1 can update status
        res = client.put(f"/api/bookings/{b_id}", json={"status": "cancelled"}, headers=renter1_headers)
        assert res.status_code == 200
        assert res.json()["status"] == "cancelled"
        
        # 5. Walk-in booking validations
        # Invalid walk-in payload (missing payment_method) -> 400
        res = client.post("/api/bookings/walk-in", json={
            "property_id": prop.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 2,
            "walk_in_guest_name": "Mary Jane"
        }, headers=owner_headers)
        assert res.status_code == 400
        
        # Renter trying walk-in booking -> 403 Forbidden
        res = client.post("/api/bookings/walk-in", json={
            "property_id": prop.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 2,
            "payment_method": "cash",
            "walk_in_guest_name": "Mary Jane"
        }, headers=renter1_headers)
        assert res.status_code == 403
        
        # Valid walk-in booking by owner -> 201 Created
        res = client.post("/api/bookings/walk-in", json={
            "property_id": prop.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 2,
            "payment_method": "mobile_money",
            "walk_in_guest_name": "Mary Jane",
            "walk_in_guest_phone": "+260979876543"
        }, headers=owner_headers)
        assert res.status_code == 201
        walkin_id = res.json()["id"]
        
        # 6. GET availability endpoint (/api/bookings/apartment/{id}/availability)
        res = client.get(f"/api/bookings/apartment/{prop.id}/availability?check_in={check_in}&check_out={check_out}")
        assert res.status_code == 200
        assert res.json()["is_available"] is False # Walk-in booking blocks dates
        
        # 7. GET /api/bookings/owner/{owner_id}/bookings
        # Owner views own -> 200 OK
        res = client.get(f"/api/bookings/owner/{owner.id}/bookings", headers=owner_headers)
        assert res.status_code == 200
        assert len(res.json()) >= 1
        
        # Renter views owner bookings -> 403 Forbidden
        res = client.get(f"/api/bookings/owner/{owner.id}/bookings", headers=renter1_headers)
        assert res.status_code == 403
        
        # 8. DELETE /api/bookings/{booking_id}
        # Unauthorized renter2 cannot delete -> 403
        res = client.delete(f"/api/bookings/{b_id}", headers=renter2_headers)
        assert res.status_code == 403
        
        # Renter1 deletes own booking -> 204 No Content
        res = client.delete(f"/api/bookings/{b_id}", headers=renter1_headers)
        assert res.status_code == 204
        
    finally:
        db.close()

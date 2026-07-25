import sys
import os
from datetime import date, timedelta, datetime
from fastapi.testclient import TestClient

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property
from app.core.security import create_access_token

client = TestClient(app)

def test_fixed_availability():
    print("=== Testing Fixed Availability ===")
    
    # Ensure database schema is initialized
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Create test owner
        ts = int(datetime.now().timestamp())
        owner_email = f"owner_avail_{ts}@example.com"
        owner = User(
            email=owner_email,
            hashed_password="hashed_password",
            full_name="Availability Owner",
            role="owner",
            is_active=True
        )
        db.add(owner)
        
        # Create test renter for placing the booking
        renter_email = f"renter_avail_{ts}@example.com"
        renter = User(
            email=renter_email,
            hashed_password="hashed_password",
            full_name="Availability Renter",
            role="renter",
            is_active=True
        )
        db.add(renter)
        
        db.commit()
        db.refresh(owner)
        db.refresh(renter)
        
        # Create test property
        test_prop = Property(
            title="Test Penthouse Suite",
            description="Luxury apartment for availability testing",
            address="123 Great East Road",
            city="Lusaka",
            price_per_night=150.00,
            capacity=4,
            bedrooms=2,
            bathrooms=2,
            owner_id=owner.id,
            property_type="apartment",
            is_available=True
        )
        db.add(test_prop)
        db.commit()
        db.refresh(test_prop)
        
        # Use dates in the future
        future_date = date.today() + timedelta(days=40)
        check_in = future_date
        check_out = future_date + timedelta(days=2)
        
        print(f"Testing dates: {check_in} to {check_out} for Property ID {test_prop.id}")
        
        # 1. Test availability endpoint (public)
        availability_response = client.get(
            f"/api/bookings/apartment/{test_prop.id}/availability",
            params={"check_in": str(check_in), "check_out": str(check_out)}
        )
        assert availability_response.status_code == 200, f"Availability check failed: {availability_response.text}"
        
        availability = availability_response.json()
        print(f"✅ Availability check: {availability['is_available']}")
        assert availability['is_available'] is True, "Property should be available"
        
        # 2. Test creating booking with authenticated user token
        renter_token = create_access_token({"sub": renter.email})
        headers = {"Authorization": f"Bearer {renter_token}"}
        
        booking_data = {
            "property_id": test_prop.id,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "guests": 2
        }
        
        booking_response = client.post("/api/bookings/", json=booking_data, headers=headers)
        assert booking_response.status_code in [200, 201], f"Booking failed: {booking_response.text}"
        
        booking = booking_response.json()
        print(f"✅ Booking created successfully! ID: {booking['id']}")
        assert booking['id'] is not None
        
    finally:
        db.close()

if __name__ == "__main__":
    test_fixed_availability()
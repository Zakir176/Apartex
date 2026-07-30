import sys
import os
from datetime import date, timedelta, datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Booking, Review
from app.core.security import create_access_token

client = TestClient(app)

def test_reviews_full_flow():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"rev_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Review Owner",
            role="owner",
            is_active=True
        )
        renter1 = User(
            email=f"rev_renter1_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Review Guest 1",
            role="renter",
            is_active=True
        )
        renter2 = User(
            email=f"rev_renter2_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Review Guest 2",
            role="renter",
            is_active=True
        )
        db.add_all([owner, renter1, renter2])
        db.commit()
        db.refresh(owner)
        db.refresh(renter1)
        db.refresh(renter2)
        
        prop = Property(
            title="Review Test Penthouse",
            description="Luxury apartment for testing reviews",
            address="100 Great East Rd",
            city="Lusaka",
            price_per_night=300.0,
            capacity=4,
            bedrooms=2,
            bathrooms=2,
            owner_id=owner.id,
            property_type="apartment",
            is_available=True
        )
        db.add(prop)
        db.commit()
        db.refresh(prop)
        
        token1 = create_access_token({"sub": renter1.email})
        token2 = create_access_token({"sub": renter2.email})
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # 1. GET empty reviews list
        res = client.get(f"/api/reviews/apartment/{prop.id}")
        assert res.status_code == 200
        assert res.json() == []
        
        # 2. Try leaving a review without having booked -> 403 Forbidden
        rev_payload = {
            "apartment_id": prop.id,
            "rating": 5,
            "comment": "Unverified attempt",
            "image_urls": []
        }
        res = client.post("/api/reviews/", json=rev_payload, headers=headers1)
        assert res.status_code == 403
        assert "must have booked" in res.json()["detail"]
        
        # 3. Create a confirmed booking for renter1
        booking = Booking(
            property_id=prop.id,
            user_id=renter1.id,
            check_in=date.today() - timedelta(days=5),
            check_out=date.today() - timedelta(days=2),
            guests=2,
            total_price=900.0,
            status="completed"
        )
        db.add(booking)
        db.commit()
        
        # 4. Leave review with image URLs for renter1 -> 201 Created
        rev_payload_valid = {
            "apartment_id": prop.id,
            "rating": 5,
            "comment": "Exceeded all expectations! Solar backup worked perfectly.",
            "image_urls": ["/static/uploads/pool.jpg", "/static/uploads/view.jpg"]
        }
        res = client.post("/api/reviews/", json=rev_payload_valid, headers=headers1)
        assert res.status_code == 201
        data = res.json()
        assert data["rating"] == 5
        assert data["is_verified"] is True
        assert len(data["images"]) == 2
        assert data["images"][0]["image_url"] == "/static/uploads/pool.jpg"
        
        # 5. Try leaving duplicate review for renter1 -> 400 Bad Request
        res = client.post("/api/reviews/", json=rev_payload_valid, headers=headers1)
        assert res.status_code == 400
        assert "already reviewed" in res.json()["detail"]
        
        # 6. Unauthenticated review attempt -> 401 Unauthorized
        res = client.post("/api/reviews/", json=rev_payload_valid)
        assert res.status_code == 401
        
        # 7. GET reviews list again -> should contain 1 review
        res = client.get(f"/api/reviews/apartment/{prop.id}")
        assert res.status_code == 200
        reviews_list = res.json()
        assert len(reviews_list) == 1
        assert reviews_list[0]["comment"] == "Exceeded all expectations! Solar backup worked perfectly."
        
    finally:
        db.close()

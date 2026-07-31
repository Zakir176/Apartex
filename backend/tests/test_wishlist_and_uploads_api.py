import sys
import os
import io
from datetime import datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Wishlist
from app.core.security import create_access_token

client = TestClient(app)

def test_wishlist_and_uploads_flow():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"w_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Wishlist Host",
            role="owner",
            is_active=True
        )
        renter = User(
            email=f"w_renter_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Wishlist Guest",
            role="renter",
            is_active=True
        )
        db.add_all([owner, renter])
        db.commit()
        db.refresh(owner)
        db.refresh(renter)
        
        prop = Property(
            title="Wishlist Test Apartment",
            description="Nice apartment",
            address="789 Park St",
            city="Lusaka",
            price_per_night=150.0,
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
        
        renter_headers = {"Authorization": f"Bearer {create_access_token({'sub': renter.email})}"}
        
        # 1. GET empty wishlist
        res = client.get("/api/wishlist/", headers=renter_headers)
        assert res.status_code == 200
        assert res.json() == []
        
        # 2. Add property to wishlist -> 201 Created
        res = client.post("/api/wishlist/", json={"apartment_id": prop.id}, headers=renter_headers)
        assert res.status_code == 201
        assert res.json()["apartment_id"] == prop.id
        
        # 3. Duplicate add attempt -> 400 Bad Request
        res = client.post("/api/wishlist/", json={"apartment_id": prop.id}, headers=renter_headers)
        assert res.status_code == 400
        assert "already in wishlist" in res.json()["detail"]
        
        # 4. GET wishlist -> 1 item
        res = client.get("/api/wishlist/", headers=renter_headers)
        assert res.status_code == 200
        assert len(res.json()) == 1
        
        # 5. Remove from wishlist -> 204 No Content
        res = client.delete(f"/api/wishlist/{prop.id}", headers=renter_headers)
        assert res.status_code == 204
        
        # 6. Remove non-existent -> 404 Not Found
        res = client.delete(f"/api/wishlist/{prop.id}", headers=renter_headers)
        assert res.status_code == 404
        
        # 7. Upload invalid file type -> 400 Bad Request
        text_file = io.BytesIO(b"Hello world")
        res = client.post(
            "/api/upload/images",
            files={"file": ("test.txt", text_file, "text/plain")},
            headers=renter_headers
        )
        assert res.status_code == 400
        assert "Only image files" in res.json()["detail"]
        
        # 8. Upload valid image file -> 200 OK
        img_file = io.BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01")
        res = client.post(
            "/api/upload/images",
            files={"file": ("test.png", img_file, "image/png")},
            headers=renter_headers
        )
        assert res.status_code == 200
        assert res.json()["url"].startswith("/static/uploads/")
        
    finally:
        db.close()

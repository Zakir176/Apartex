import sys
import os
from datetime import datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property
from app.core.security import create_access_token

client = TestClient(app)

def test_apartments_full_crud_and_filters():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"apt_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Apartment Owner",
            role="owner",
            is_active=True
        )
        other_owner = User(
            email=f"apt_other_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Other Owner",
            role="owner",
            is_active=True
        )
        renter = User(
            email=f"apt_renter_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Apartment Guest",
            role="renter",
            is_active=True
        )
        db.add_all([owner, other_owner, renter])
        db.commit()
        db.refresh(owner)
        db.refresh(other_owner)
        db.refresh(renter)
        
        owner_headers = {"Authorization": f"Bearer {create_access_token({'sub': owner.email})}"}
        other_headers = {"Authorization": f"Bearer {create_access_token({'sub': other_owner.email})}"}
        renter_headers = {"Authorization": f"Bearer {create_access_token({'sub': renter.email})}"}
        
        # 1. Renter trying to create property -> 403 Forbidden
        payload = {
            "title": "Unapproved Villa",
            "description": "Luxury villa",
            "address": "123 Main St",
            "city": "Lusaka",
            "price_per_night": 180.0,
            "capacity": 4,
            "bedrooms": 2,
            "bathrooms": 2,
            "property_type": "apartment",
            "amenities": ["WiFi", "Pool"]
        }
        res = client.post("/api/properties/", json=payload, headers=renter_headers)
        assert res.status_code == 403
        
        # 2. Owner creates property -> 200 OK
        res = client.post("/api/properties/", json=payload, headers=owner_headers)
        assert res.status_code == 200
        prop_data = res.json()
        prop_id = prop_data["id"]
        assert prop_data["title"] == "Unapproved Villa"
        assert "WiFi" in prop_data["amenities"]
        
        # 3. GET /api/properties/me as owner -> returns 1 property
        res = client.get("/api/properties/me", headers=owner_headers)
        assert res.status_code == 200
        my_list = res.json()
        assert len(my_list) == 1
        assert my_list[0]["id"] == prop_id
        
        # 4. GET /api/properties/me as renter -> 403 Forbidden
        res = client.get("/api/properties/me", headers=renter_headers)
        assert res.status_code == 403
        
        # 5. GET /api/properties/{id}
        res = client.get(f"/api/properties/{prop_id}")
        assert res.status_code == 200
        assert res.json()["id"] == prop_id
        
        # GET non-existent -> 404
        res = client.get("/api/properties/999999")
        assert res.status_code == 404
        
        # 6. Filter listings by owner_id
        res = client.get(f"/api/properties/?owner_id={owner.id}")
        assert res.status_code == 200
        assert any(p["id"] == prop_id for p in res.json())
        
        # 7. Update property as other owner -> 403 Forbidden
        update_payload = {"title": "Hacked Villa Title"}
        res = client.put(f"/api/properties/{prop_id}", json=update_payload, headers=other_headers)
        assert res.status_code == 403
        
        # Update property as owner -> 200 OK
        update_payload_valid = {"title": "Rhodes Park Executive Suite", "price_per_night": 220.0}
        res = client.put(f"/api/properties/{prop_id}", json=update_payload_valid, headers=owner_headers)
        assert res.status_code == 200
        assert res.json()["title"] == "Rhodes Park Executive Suite"
        assert res.json()["price_per_night"] == 220.0
        
        # 8. Delete property as other owner -> 403 Forbidden
        res = client.delete(f"/api/properties/{prop_id}", headers=other_headers)
        assert res.status_code == 403
        
        # Delete property as owner -> 204 No Content
        res = client.delete(f"/api/properties/{prop_id}", headers=owner_headers)
        assert res.status_code == 204
        
        # Verify deletion
        res = client.get(f"/api/properties/{prop_id}")
        assert res.status_code == 404
        
    finally:
        db.close()

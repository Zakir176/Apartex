import sys
import os
from datetime import date, timedelta, datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, BlockedDate
from app.core.security import create_access_token

client = TestClient(app)

def test_availability_manual_blocking_flow():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"avail_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Availability Owner",
            role="owner",
            is_active=True
        )
        other_owner = User(
            email=f"avail_other_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Other Owner",
            role="owner",
            is_active=True
        )
        db.add_all([owner, other_owner])
        db.commit()
        db.refresh(owner)
        db.refresh(other_owner)
        
        prop = Property(
            title="Availability Test Villa",
            description="Villa for blocked dates testing",
            address="500 Park Lane",
            city="Lusaka",
            price_per_night=250.0,
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
        
        owner_headers = {"Authorization": f"Bearer {create_access_token({'sub': owner.email})}"}
        other_headers = {"Authorization": f"Bearer {create_access_token({'sub': other_owner.email})}"}
        
        start_d = date.today() + timedelta(days=10)
        end_d = date.today() + timedelta(days=12)
        
        # 1. Invalid date range (start > end) -> 400 Bad Request
        invalid_payload = {
            "apartment_id": prop.id,
            "start_date": str(end_d),
            "end_date": str(start_d),
            "reason": "maintenance"
        }
        res = client.post("/api/availability/block", json=invalid_payload, headers=owner_headers)
        assert res.status_code == 400
        
        # 2. Non-owner block attempt -> 403 Forbidden
        valid_payload = {
            "apartment_id": prop.id,
            "start_date": str(start_d),
            "end_date": str(end_d),
            "reason": "maintenance"
        }
        res = client.post("/api/availability/block", json=valid_payload, headers=other_headers)
        assert res.status_code == 403
        
        # 3. Owner blocks date range (3 days) -> 201 Created
        res = client.post("/api/availability/block", json=valid_payload, headers=owner_headers)
        assert res.status_code == 201
        blocked_list = res.json()
        assert len(blocked_list) == 3
        block_id_to_delete = blocked_list[0]["id"]
        
        # 4. GET /api/availability/{apartment_id} -> returns 3 blocked dates
        res = client.get(f"/api/availability/{prop.id}")
        assert res.status_code == 200
        assert len(res.json()) == 3
        
        # 5. Non-owner unblock attempt -> 403 Forbidden
        res = client.delete(f"/api/availability/{block_id_to_delete}", headers=other_headers)
        assert res.status_code == 403
        
        # 6. Owner unblocks 1 date -> 204 No Content
        res = client.delete(f"/api/availability/{block_id_to_delete}", headers=owner_headers)
        assert res.status_code == 204
        
        # Verify remaining count is 2
        res = client.get(f"/api/availability/{prop.id}")
        assert res.status_code == 200
        assert len(res.json()) == 2
        
    finally:
        db.close()

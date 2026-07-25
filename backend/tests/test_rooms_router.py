import sys
import os
from datetime import datetime
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Room
from app.routers.auth_enhanced import create_access_token

client = TestClient(app)

def test_rooms_router_endpoints():
    print("=== Testing Rooms Router Endpoints ===")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"room_router_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Room Router Owner",
            role="owner",
            is_active=True
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
        
        prop = Property(
            title="Kabwe Grand Hotel",
            description="Luxury hotel in Kabwe",
            address="Great North Road",
            city="Kabwe",
            price_per_night=300.00,
            capacity=20,
            bedrooms=10,
            bathrooms=10,
            owner_id=owner.id,
            property_type="hotel",
            is_available=True
        )
        db.add(prop)
        db.commit()
        db.refresh(prop)
        
        token = create_access_token(data={"sub": owner.email})
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Create Room (POST /api/rooms/)
        room_payload = {
            "property_id": prop.id,
            "room_type": "Presidential Suite",
            "description": "Top floor view with jacuzzi",
            "price_per_night": 250.00,
            "capacity": 2,
            "total_units": 2,
            "amenities": '["Jacuzzi", "King Bed", "WiFi"]',
            "is_available": True
        }
        res = client.post("/api/rooms/", json=room_payload, headers=headers)
        assert res.status_code == 201, f"Create room failed: {res.text}"
        room_data = res.json()
        room_id = room_data["id"]
        assert room_data["room_type"] == "Presidential Suite"
        print(f"✅ Created Room via API: ID {room_id}")
        
        # 2. Get Rooms for Property (GET /api/rooms/property/{property_id})
        res = client.get(f"/api/rooms/property/{prop.id}")
        assert res.status_code == 200
        rooms_list = res.json()
        assert len(rooms_list) >= 1
        print("✅ Fetched public rooms for property")
        
        # 3. Get Owner Rooms (GET /api/rooms/my/property/{property_id})
        res = client.get(f"/api/rooms/my/property/{prop.id}", headers=headers)
        assert res.status_code == 200
        print("✅ Fetched owner rooms")
        
        # 4. Get Single Room (GET /api/rooms/{room_id})
        res = client.get(f"/api/rooms/{room_id}")
        assert res.status_code == 200
        assert res.json()["id"] == room_id
        print("✅ Fetched single room")
        
        # 5. Update Room (PUT /api/rooms/{room_id})
        update_payload = {"price_per_night": 280.00, "description": "Updated penthouse suite"}
        res = client.put(f"/api/rooms/{room_id}", json=update_payload, headers=headers)
        assert res.status_code == 200
        assert res.json()["price_per_night"] == 280.00
        print("✅ Updated room via API")
        
        # 6. Delete Room (DELETE /api/rooms/{room_id})
        res = client.delete(f"/api/rooms/{room_id}", headers=headers)
        assert res.status_code == 204
        print("✅ Deleted room via API")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_rooms_router_endpoints()

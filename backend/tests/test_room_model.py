import sys
import os
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Room

def test_room_model_crud():
    print("=== Testing Room Model CRUD ===")
    
    # Ensure database schema is initialized
    Base.metadata.create_all(bind=engine)
    
    # Safely add room_id if SQLite file exists
    inspector = inspect(engine)
    if "bookings" in inspector.get_table_names():
        booking_cols = [c["name"] for c in inspector.get_columns("bookings")]
        if "room_id" not in booking_cols:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE bookings ADD COLUMN room_id INTEGER REFERENCES rooms(id)"))
                conn.commit()

    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner = User(
            email=f"room_owner_{ts}@example.com",
            hashed_password="hashed_password",
            full_name="Room Test Host",
            role="owner",
            is_active=True
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
        
        prop = Property(
            title="Livingstone Safari Lodge",
            description="Luxury lodge with chalets",
            address="Zambezi River Road",
            city="Livingstone",
            price_per_night=250.00,
            capacity=10,
            bedrooms=6,
            bathrooms=6,
            owner_id=owner.id,
            property_type="lodge",
            is_available=True
        )
        db.add(prop)
        db.commit()
        db.refresh(prop)
        
        # Create Room
        room = Room(
            property_id=prop.id,
            room_type="Executive Chalet",
            description="Private riverfront chalet with king bed and balcony",
            price_per_night=180.00,
            capacity=2,
            total_units=4,
            amenities='["River View", "Air-Con", "Breakfast Included"]',
            is_available=True
        )
        db.add(room)
        db.commit()
        db.refresh(room)
        
        assert room.id is not None
        assert room.room_type == "Executive Chalet"
        assert room.property.title == "Livingstone Safari Lodge"
        assert len(prop.rooms) == 1
        print(f"✅ Room created successfully! ID: {room.id}, Type: {room.room_type}")

    finally:
        db.close()

if __name__ == "__main__":
    test_room_model_crud()

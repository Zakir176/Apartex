from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from sqlalchemy import inspect, Column, String, text
from app.models import user, apartment, booking, loyalty, payout, wishlist, review, apartment_image, blocked_date, room
from app.routers import apartments, bookings, loyalty as loyalty_router, dashboard, auth_enhanced, wishlist as wishlist_router, reviews, availability
from app.routers import rooms as rooms_router
from app.routers import uploads

import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Apartex API", version="1.0.0")

from app.models.room import Room
from app.models.apartment import Property
from sqlalchemy.orm import Session
from app.database import SessionLocal

def seed_demo_rooms():
    db: Session = SessionLocal()
    try:
        if db.query(Room).count() == 0:
            # Get all non-apartment properties
            properties = db.query(Property).filter(
                Property.property_type.in_(["hotel", "lodge", "guest_house"])
            ).all()
            for prop in properties:
                rooms = [
                    Room(property_id=prop.id, room_type="Standard Room", price_per_night=float(prop.price_per_night), capacity=2, total_units=5, description="Comfortable standard room with all essentials"),
                    Room(property_id=prop.id, room_type="Deluxe Room", price_per_night=float(prop.price_per_night) * 1.4, capacity=2, total_units=3, description="Spacious deluxe room with premium amenities"),
                    Room(property_id=prop.id, room_type="Family Suite", price_per_night=float(prop.price_per_night) * 1.8, capacity=4, total_units=2, description="Large suite ideal for families"),
                ]
                db.add_all(rooms)
            db.commit()
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    """Run schema creation & migrations safely on startup."""
    try:
        Base.metadata.create_all(bind=engine)
        
        # Safely add missing columns to SQLite database if needed
        inspector = inspect(engine)
        if "bookings" in inspector.get_table_names():
            booking_cols = [c["name"] for c in inspector.get_columns("bookings")]
            if "room_id" not in booking_cols:
                with engine.connect() as conn:
                    conn.execute(text("ALTER TABLE bookings ADD COLUMN room_id INTEGER REFERENCES rooms(id)"))
                    conn.commit()
                logger.info("Added room_id column to bookings table.")
        
        seed_demo_rooms()
    except Exception as e:
        logger.error("Error during startup schema initialization", exc_info=True)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "https://apartex.vercel.app"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Include routers with /api prefix
app.include_router(auth_enhanced.router, prefix="/api/auth-enhanced", tags=["authentication-enhanced"])
app.include_router(apartments.router, prefix="/api/properties", tags=["properties"])
app.include_router(rooms_router.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])
app.include_router(loyalty_router.router, prefix="/api/loyalty", tags=["loyalty"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(uploads.router, prefix="/api/upload", tags=["uploads"])
app.include_router(wishlist_router.router, prefix="/api/wishlist", tags=["wishlist"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(availability.router, prefix="/api/availability", tags=["availability"])

# v1 backwards compatibility alias — keep /api/apartments/ working
from app.routers import apartments as apartments_v1_alias
app.include_router(apartments_v1_alias.router, prefix="/api/apartments", tags=["apartments-v1-alias"], include_in_schema=False)

# Static files for uploads (ONLY point to uploads directory for security)
import os
uploads_dir = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/")
def read_root():
    return {"message": "Apartex API is running!"}
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

def seed_all_demo_data():
    """
    Seeds demo properties covering all four property types with realistic
    Zambian locations and room types for hotels/lodges/guest houses.
    Only runs if the properties table has fewer than 6 entries.
    """
    db: Session = SessionLocal()
    try:
        existing_count = db.query(Property).count()
        if existing_count >= 6:
            seed_demo_rooms(db)
            return

        from app.models.user import User
        import bcrypt

        # Create a demo owner if none exists
        owner = db.query(User).filter(User.role == "owner").first()
        if not owner:
            hashed = bcrypt.hashpw("demo1234".encode(), bcrypt.gensalt()).decode()
            owner = User(
                email="owner@apartex.zm",
                full_name="Demo Owner",
                hashed_password=hashed,
                role="owner",
            )
            db.add(owner)
            db.flush()

        # ── Apartments ──────────────────────────────────────────────────────
        apartments_data = [
            {
                "title": "Modern Studio in Kabulonga",
                "description": "A bright, fully-furnished studio apartment in the heart of Kabulonga. Walking distance to restaurants, shops and supermarkets. High-speed WiFi, backup power and secure parking included.",
                "address": "14 Birdcage Walk, Kabulonga, Lusaka",
                "city": "Lusaka",
                "price_per_night": 85.00,
                "capacity": 2,
                "bedrooms": 1,
                "bathrooms": 1,
                "property_type": "apartment",
                "amenities": '["WiFi", "Air Conditioning", "Parking", "Backup Power", "Kitchen", "Security"]',
                "image_url": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
                "latitude": -15.3875, "longitude": 28.3228,
            },
            {
                "title": "Luxury 3-Bed Apartment, Rhodespark",
                "description": "Spacious three-bedroom apartment in the upmarket Rhodespark area. Fully serviced, with a swimming pool, gym access and 24-hour security.",
                "address": "23 Cheetah Road, Rhodespark, Lusaka",
                "city": "Lusaka",
                "price_per_night": 180.00,
                "capacity": 6,
                "bedrooms": 3,
                "bathrooms": 2,
                "property_type": "apartment",
                "amenities": '["WiFi", "Pool", "Gym", "Air Conditioning", "Parking", "Backup Power", "Kitchen", "Security", "Laundry"]',
                "image_url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800",
                "latitude": -15.4100, "longitude": 28.2980,
            },
        ]

        # ── Hotels ───────────────────────────────────────────────────────────
        hotels_data = [
            {
                "title": "Savanna Business Hotel",
                "description": "A premier business hotel in central Lusaka with conference facilities, restaurant and rooftop bar. Ideal for corporate travellers and long-stay guests.",
                "address": "Cairo Road, Central Business District, Lusaka",
                "city": "Lusaka",
                "price_per_night": 120.00,
                "capacity": 80,
                "bedrooms": 0,
                "bathrooms": 0,
                "property_type": "hotel",
                "star_rating": 4,
                "amenities": '["WiFi", "Restaurant", "Bar", "Conference Room", "Pool", "Gym", "Parking", "Room Service", "24hr Reception"]',
                "image_url": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800",
                "latitude": -15.4166, "longitude": 28.2833,
            },
        ]

        # ── Lodges ───────────────────────────────────────────────────────────
        lodges_data = [
            {
                "title": "Victoria Falls River Lodge",
                "description": "Breathtaking lodge perched on the Zambezi River just upstream from Victoria Falls. Canoe excursions, game drives and sunset cruises available daily. A true African safari experience.",
                "address": "Zambezi Drive, Livingstone",
                "city": "Livingstone",
                "price_per_night": 220.00,
                "capacity": 40,
                "bedrooms": 0,
                "bathrooms": 0,
                "property_type": "lodge",
                "star_rating": 5,
                "amenities": '["WiFi", "Restaurant", "Bar", "Game Drives", "Canoe Excursions", "Sunset Cruises", "Pool", "Laundry", "Backup Power"]',
                "image_url": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=800",
                "latitude": -17.9244, "longitude": 25.8572,
            },
            {
                "title": "Kafue Bush Camp",
                "description": "An intimate bush camp within the Kafue National Park. Six luxury tented chalets with en-suite bathrooms and private verandas overlooking a seasonal floodplain. Full board available.",
                "address": "Kafue National Park, Itezhi-Tezhi",
                "city": "Itezhi-Tezhi",
                "price_per_night": 195.00,
                "capacity": 20,
                "bedrooms": 0,
                "bathrooms": 0,
                "property_type": "lodge",
                "star_rating": 4,
                "amenities": '["Full Board", "Game Drives", "Bush Walks", "WiFi", "Backup Power", "Laundry", "Bar"]',
                "image_url": "https://images.unsplash.com/photo-1535941339077-2dd1c7963098?w=800",
                "latitude": -15.7811, "longitude": 26.0145,
            },
        ]

        # ── Guest Houses ─────────────────────────────────────────────────────
        guest_houses_data = [
            {
                "title": "Ndola Garden Guest House",
                "description": "A warm, homely guest house on a quiet tree-lined street in Ndola. Breakfast included, laundry available, and airport transfers arranged on request.",
                "address": "12 Buteko Avenue, Ndola",
                "city": "Ndola",
                "price_per_night": 55.00,
                "capacity": 16,
                "bedrooms": 0,
                "bathrooms": 0,
                "property_type": "guest_house",
                "amenities": '["WiFi", "Breakfast Included", "Parking", "Laundry", "Airport Transfer", "Security"]',
                "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800",
                "latitude": -12.9587, "longitude": 28.6366,
            },
        ]

        all_properties_data = apartments_data + hotels_data + lodges_data + guest_houses_data
        created_properties = []

        for prop_data in all_properties_data:
            prop = Property(
                owner_id=owner.id,
                is_available=True,
                **prop_data
            )
            db.add(prop)
            db.flush()
            created_properties.append(prop)

        db.commit()
        logger.info(f"Seeded {len(created_properties)} demo properties.")

        # ── Seed rooms for non-apartment properties ──────────────────────────
        seed_demo_rooms(db)

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding demo data: {e}", exc_info=True)
    finally:
        db.close()


def seed_demo_rooms(db: Session = None):
    """Seeds room types for hotel, lodge, and guest house properties."""
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        if db.query(Room).count() > 0:
            return

        non_apartment_properties = db.query(Property).filter(
            Property.property_type.in_(["hotel", "lodge", "guest_house"])
        ).all()

        room_templates = {
            "hotel": [
                {"room_type": "Standard Room", "price_multiplier": 1.0, "capacity": 2, "total_units": 10,
                 "description": "Comfortable en-suite room with king or twin beds, air conditioning, flat-screen TV and complimentary WiFi.",
                 "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600"},
                {"room_type": "Deluxe Room", "price_multiplier": 1.4, "capacity": 2, "total_units": 6,
                 "description": "Spacious deluxe room with upgraded furnishings, mini-bar and city views.",
                 "image_url": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=600"},
                {"room_type": "Executive Suite", "price_multiplier": 2.0, "capacity": 2, "total_units": 3,
                 "description": "Full suite with separate lounge area, work desk, premium toiletries and express check-in.",
                 "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=600"},
                {"room_type": "Family Room", "price_multiplier": 1.6, "capacity": 4, "total_units": 4,
                 "description": "Spacious family room with one double bed and two singles, perfect for families travelling together.",
                 "image_url": "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=600"},
            ],
            "lodge": [
                {"room_type": "Standard Chalet", "price_multiplier": 1.0, "capacity": 2, "total_units": 4,
                 "description": "Tented chalet with en-suite bathroom, twin or double beds and a private veranda overlooking the bush.",
                 "image_url": "https://images.unsplash.com/photo-1510798831971-661eb04b3739?w=600"},
                {"room_type": "Luxury Chalet", "price_multiplier": 1.5, "capacity": 2, "total_units": 3,
                 "description": "Premium tented suite with outdoor shower, plunge pool and butler service. The ultimate bush experience.",
                 "image_url": "https://images.unsplash.com/photo-1506059612708-99d6c258160e?w=600"},
                {"room_type": "Family Chalet", "price_multiplier": 1.8, "capacity": 4, "total_units": 2,
                 "description": "Two interconnected chalets ideal for families, with a shared lounge and private outdoor dining area.",
                 "image_url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600"},
            ],
            "guest_house": [
                {"room_type": "Single Room", "price_multiplier": 1.0, "capacity": 1, "total_units": 4,
                 "description": "Cosy single room with en-suite or shared bathroom. Breakfast included. Perfect for solo travellers.",
                 "image_url": "https://images.unsplash.com/photo-1505693314120-0d443867891c?w=600"},
                {"room_type": "Double Room", "price_multiplier": 1.4, "capacity": 2, "total_units": 4,
                 "description": "Double room with private bathroom, wardrobe and desk. Breakfast included.",
                 "image_url": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=600"},
                {"room_type": "Self-Catering Room", "price_multiplier": 1.6, "capacity": 2, "total_units": 2,
                 "description": "Room with attached kitchenette — fridge, microwave, and basic cooking utensils provided. Ideal for longer stays.",
                 "image_url": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600"},
            ],
        }

        total_rooms = 0
        for prop in non_apartment_properties:
            templates = room_templates.get(prop.property_type, [])
            for template in templates:
                multiplier = template.pop("price_multiplier")
                room = Room(
                    property_id=prop.id,
                    price_per_night=round(float(prop.price_per_night) * multiplier, 2),
                    **template,
                )
                template["price_multiplier"] = multiplier  # restore for next property
                db.add(room)
                total_rooms += 1

        db.commit()
        logger.info(f"Seeded {total_rooms} demo rooms across {len(non_apartment_properties)} properties.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding demo rooms: {e}", exc_info=True)
    finally:
        if close_db:
            db.close()


@app.on_event("startup")
async def startup_event():
    """Run schema creation and seed demo data on startup."""
    try:
        Base.metadata.create_all(bind=engine)

        # Ensure room_id column exists on bookings (safe migration for existing DBs)
        inspector = inspect(engine)
        if "bookings" in inspector.get_table_names():
            booking_cols = [c["name"] for c in inspector.get_columns("bookings")]
            if "room_id" not in booking_cols:
                with engine.connect() as conn:
                    conn.execute(text("ALTER TABLE bookings ADD COLUMN room_id INTEGER REFERENCES rooms(id)"))
                    conn.commit()
                logger.info("Added room_id column to bookings table.")

        seed_all_demo_data()

    except Exception as e:
        logger.error("Error during startup", exc_info=True)


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
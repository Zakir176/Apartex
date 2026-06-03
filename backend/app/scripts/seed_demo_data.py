# backend/app/scripts/seed_demo_data.py
"""
Seed demo data for Apartex.

Usage (from backend folder):
    python -m app.scripts.seed_demo_data
"""

from datetime import datetime, timedelta
import traceback
import json

from app.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.user import User
from app.models.apartment import Apartment
from app.models.booking import Booking
from app.models.payout import Payout
from app.models.wishlist import Wishlist
from app.models.review import Review
from app.models.loyalty import LoyaltyReward
from app.models.blocked_date import BlockedDate
from app.models.apartment_image import ApartmentImage

def create_tables():
    """Ensure DB tables exist."""
    Base.metadata.create_all(bind=engine)
    print("✅ Ensured tables exist (Base.metadata.create_all)")

def seed_demo_data():
    db = SessionLocal()
    try:
        print("🌱 Starting seeding demo data...")

        # --- 1) Owner user ---
        owner_email = "demo_owner@apartex.com"
        owner = db.query(User).filter(User.email == owner_email).first()
        if not owner:
            owner = User(
                email=owner_email,
                full_name="Demo Owner",
                hashed_password=hash_password("owner123"),
                role="owner",
            )
            db.add(owner)
            db.commit()
            db.refresh(owner)
            print(f"Created owner: id={owner.id} email={owner.email}")
        else:
            print(f"Owner already exists: id={owner.id} email={owner.email}")

        # --- 2) Renter user ---
        renter_email = "demo_renter@apartex.com"
        renter = db.query(User).filter(User.email == renter_email).first()
        if not renter:
            renter = User(
                email=renter_email,
                full_name="Demo Renter",
                hashed_password=hash_password("renter123"),
                role="renter",
            )
            db.add(renter)
            db.commit()
            db.refresh(renter)
            print(f"Created renter: id={renter.id} email={renter.email}")
        else:
            print(f"Renter already exists: id={renter.id} email={renter.email}")

        # --- 3) apartments ---
        apt1_title = "Luxury City Apartment"
        apt2_title = "Cozy Riverside Cottage"

        apt1 = db.query(Apartment).filter(Apartment.title == apt1_title).first()
        if not apt1:
            apt1 = Apartment(
                title=apt1_title,
                description="Modern apartment with city view",
                address="123 Independence Ave",
                city="Lusaka",
                price_per_night=150.0,
                capacity=2,
                bedrooms=1,
                bathrooms=1,
                amenities=json.dumps(["WiFi", "AC", "Kitchen"]),
                latitude=-15.3875,
                longitude=28.3228,
                owner_id=owner.id,
            )
            db.add(apt1)
            db.commit()
            db.refresh(apt1)
            print(f"Created apartment 1 id={apt1.id} title={apt1.title}")
        else:
            print(f"Apt1 already exists id={apt1.id}")

        apt2 = db.query(Apartment).filter(Apartment.title == apt2_title).first()
        if not apt2:
            apt2 = Apartment(
                title=apt2_title,
                description="Peaceful cottage near the river",
                address="456 River Bank Road",
                city="Livingstone",
                price_per_night=100.0,
                capacity=4,
                bedrooms=2,
                bathrooms=1,
                amenities=json.dumps(["WiFi", "Fireplace", "View"]),
                latitude=-16.8561,
                longitude=25.8528,
                owner_id=owner.id,
            )
            db.add(apt2)
            db.commit()
            db.refresh(apt2)
            print(f"Created apartment 2 id={apt2.id} title={apt2.title}")
        else:
            print(f"Apt2 already exists id={apt2.id}")

        # --- 4) bookings (some completed, some upcoming) ---
        today = datetime.utcnow().date()

        # Completed booking on apt1
        b1 = db.query(Booking).filter(
            Booking.apartment_id == apt1.id,
            Booking.check_in == today - timedelta(days=30),
            Booking.check_out == today - timedelta(days=25)
        ).first()
        if not b1:
            b1 = Booking(
                apartment_id=apt1.id,
                user_id=renter.id,
                check_in=today - timedelta(days=30),
                check_out=today - timedelta(days=25),
                total_price=750.0,
                status="completed"
            )
            db.add(b1)
            db.commit()
            print(f"Created booking 1 id={b1.id}")
        else:
            print(f"booking1 exists id={b1.id}")

        # Completed booking on apt2
        b2 = db.query(Booking).filter(
            Booking.apartment_id == apt2.id,
            Booking.check_in == today - timedelta(days=10),
            Booking.check_out == today - timedelta(days=7)
        ).first()
        if not b2:
            b2 = Booking(
                apartment_id=apt2.id,
                user_id=renter.id,
                check_in=today - timedelta(days=10),
                check_out=today - timedelta(days=7),
                total_price=300.0,
                status="completed"
            )
            db.add(b2)
            db.commit()
            print(f"Created booking 2 id={b2.id}")
        else:
            print(f"booking2 exists id={b2.id}")

        # Upcoming booking on apt1
        b3 = db.query(Booking).filter(
            Booking.apartment_id == apt1.id,
            Booking.check_in == today + timedelta(days=5),
            Booking.check_out == today + timedelta(days=8)
        ).first()
        if not b3:
            b3 = Booking(
                apartment_id=apt1.id,
                user_id=renter.id,
                check_in=today + timedelta(days=5),
                check_out=today + timedelta(days=8),
                total_price=450.0,
                status="confirmed"
            )
            db.add(b3)
            db.commit()
            print(f"Created booking 3 id={b3.id}")
        else:
            print(f"booking3 exists id={b3.id}")

        # --- 5) payouts ---
        p1 = db.query(Payout).filter(Payout.owner_id == owner.id, Payout.amount == 700.0).first()
        if not p1:
            p1 = Payout(
                owner_id=owner.id,
                amount=700.0,
                status="completed",
                period_start=today - timedelta(days=45),
                period_end=today - timedelta(days=15),
                processed_at=datetime.utcnow() - timedelta(days=15),
                created_at=datetime.utcnow() - timedelta(days=15)
            )
            db.add(p1)
            db.commit()
            print(f"Created payout 1 id={p1.id}")
        else:
            print(f"payout1 exists id={p1.id}")

        p2 = db.query(Payout).filter(Payout.owner_id == owner.id, Payout.amount == 500.0).first()
        if not p2:
            p2 = Payout(
                owner_id=owner.id,
                amount=500.0,
                status="pending",
                period_start=today - timedelta(days=14),
                period_end=today,
                created_at=datetime.utcnow()
            )
            db.add(p2)
            db.commit()
            print(f"Created payout 2 id={p2.id}")
        else:
            print(f"Payout2 exists id={p2.id}")

        print("\n🎉 Seeding complete! You can now log in with demo_owner@apartex.com / owner123")
    except Exception:
        print("ERROR while seeding demo data:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_demo_data()

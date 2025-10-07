# backend/app/scripts/seed_demo_data.py
"""
Seed demo data for Apartex.

Usage (from backend folder):
    python -m app.scripts.seed_demo_data
"""

from datetime import datetime, timedelta
import traceback

from app.database import SessionLocal, Base, engine
from app.core.security import hash_password

# Import model classes (make sure app/models/_init_.py exposes these names)
try:
    from app.models import user, apartment, booking, payout
except Exception as e:
    print("ERROR: could not import models from app.models. Verify app/models/_init_.py exports user, apartment, booking, payout.")
    print("Detailed import error:")
    traceback.print_exc()
    raise

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
        owner = db.query(user).filter(user.email == owner_email).first()
        if not owner:
            owner = user(
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
        renter = db.query(user).filter(user.email == renter_email).first()
        if not renter:
            renter = user(
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
        # Adjust the field names here if your apartment model uses different attribute names
        apt1_name = "Luxury City apartment"
        apt2_name = "Cozy Riverside Cottage"

        apt1 = db.query(apartment).filter(apartment.name == apt1_name).first()
        if not apt1:
            apt1 = apartment(
                name=apt1_name,
                description="Modern apartment with city view",
                price_per_night=150.0,
                location="Lusaka",
                owner_id=owner.id,
            )
            db.add(apt1)
            db.commit()
            db.refresh(apt1)
            print(f"Created apartment 1 id={apt1.id} name={apt1.name}")
        else:
            print(f"Apt1 already exists id={apt1.id}")

        apt2 = db.query(apartment).filter(apartment.name == apt2_name).first()
        if not apt2:
            apt2 = apartment(
                name=apt2_name,
                description="Peaceful cottage near the river",
                price_per_night=100.0,
                location="Livingstone",
                owner_id=owner.id,
            )
            db.add(apt2)
            db.commit()
            db.refresh(apt2)
            print(f"Created apartment 2 id={apt2.id} name={apt2.name}")
        else:
            print(f"Apt2 already exists id={apt2.id}")

        # --- 4) bookings (some completed, some upcoming) ---
        today = datetime.utcnow().date()

        # Completed booking on apt1
        b1 = db.query(booking).filter(
            booking.apartment_id == apt1.id,
            booking.start_date == today - timedelta(days=30),
            booking.end_date == today - timedelta(days=25)
        ).first()
        if not b1:
            b1 = booking(
                apartment_id=apt1.id,
                user_id=renter.id,
                start_date=today - timedelta(days=30),
                end_date=today - timedelta(days=25),
                total_amount=750.0,
                status="completed"
            )
            db.add(b1)
            db.commit()
            print(f"Created booking 1 id={b1.id}")
        else:
            print(f"booking1 exists id={b1.id}")

        # Completed booking on apt2
        b2 = db.query(booking).filter(
            booking.apartment_id == apt2.id,
            booking.start_date == today - timedelta(days=10),
            booking.end_date == today - timedelta(days=7)
        ).first()
        if not b2:
            b2 = booking(
                apartment_id=apt2.id,
                user_id=renter.id,
                start_date=today - timedelta(days=10),
                end_date=today - timedelta(days=7),
                total_amount=300.0,
                status="completed"
            )
            db.add(b2)
            db.commit()
            print(f"Created booking 2 id={b2.id}")
        else:
            print(f"booking2 exists id={b2.id}")

        # Upcoming booking on apt1
        b3 = db.query(booking).filter(
            booking.apartment_id == apt1.id,
            booking.start_date == today + timedelta(days=5),
            booking.end_date == today + timedelta(days=8)
        ).first()
        if not b3:
            b3 = booking(
                apartment_id=apt1.id,
                user_id=renter.id,
                start_date=today + timedelta(days=5),
                end_date=today + timedelta(days=8),
                total_amount=450.0,
                status="upcoming"
            )
            db.add(b3)
            db.commit()
            print(f"Created booking 3 id={b3.id}")
        else:
            print(f"booking3 exists id={b3.id}")

        # --- 5) payouts ---
        p1 = db.query(payout).filter(payout.owner_id == owner.id, payout.amount == 700.0).first()
        if not p1:
            p1 = payout(
                owner_id=owner.id,
                amount=700.0,
                status="paid",
                method="bank",
                created_at=datetime.utcnow() - timedelta(days=15)
            )
            db.add(p1)
            db.commit()
            print(f"Created payout 1 id={p1.id}")
        else:
            print(f"payout1 exists id={p1.id}")

        p2 = db.query(payout).filter(payout.owner_id == owner.id, payout.amount == 500.0).first()
        if not p2:
            p2 = payout(
                owner_id=owner.id,
                amount=500.0,
                status="pending",
                method="momo",
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

if __name__ == "_main_":
    create_tables()
    seed_demo_data()
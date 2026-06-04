import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import User, Apartment, Booking, Review, ReviewImage, Wishlist, LoyaltyReward, Payout

def test_advanced_reviews():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Create a test user (renter)
        test_email = f"renter_{int(datetime.now().timestamp())}@example.com"
        user = User(
            email=test_email,
            hashed_password="hashed_password",
            full_name="Test Renter",
            role="renter"
        )
        db.add(user)
        db.flush()

        # 2. Create a test apartment
        apartment = Apartment(
            title="Luxury Test Villa",
            address="123 Test St",
            city="Lusaka",
            price_per_night=250.0,
            capacity=4,
            bedrooms=2,
            bathrooms=2,
            owner_id=1 # Assuming owner with ID 1 exists
        )
        db.add(apartment)
        db.flush()

        # 3. Create a booking for this user and apartment (needed for review)
        booking = Booking(
            user_id=user.id,
            apartment_id=apartment.id,
            check_in=datetime.now().date(),
            check_out=(datetime.now() + timedelta(days=2)).date(),
            total_price=500.0,
            status="completed"
        )
        db.add(booking)
        db.flush()

        # 4. Create a review with images
        review = Review(
            apartment_id=apartment.id,
            user_id=user.id,
            rating=5,
            comment="Amazing stay! Loved the pool.",
            is_verified=True
        )
        db.add(review)
        db.flush()

        review_image = ReviewImage(
            review_id=review.id,
            image_url="/static/uploads/test_image.jpg"
        )
        db.add(review_image)
        db.commit()

        # 5. Verify data
        db.refresh(review)
        print(f"✅ Review created: ID={review.id}, Verified={review.is_verified}")
        print(f"✅ Review Images: count={len(review.images)}, first_url={review.images[0].image_url}")

        assert review.is_verified == True
        assert len(review.images) == 1
        assert review.images[0].image_url == "/static/uploads/test_image.jpg"
        
        print("🚀 Advanced Reviews verification SUCCESSFUL!")

    except Exception as e:
        db.rollback()
        print(f"❌ Verification FAILED: {str(e)}")
        raise e
    finally:
        # Cleanup (optional, but good for local dev)
        # db.delete(review_image)
        # db.delete(review)
        # db.delete(booking)
        # db.delete(apartment)
        # db.delete(user)
        # db.commit()
        db.close()

if __name__ == "__main__":
    test_advanced_reviews()

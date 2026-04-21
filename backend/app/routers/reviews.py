from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.review import Review
from app.models.booking import Booking
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate
from app.routers.auth_enhanced import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new review for an apartment.
    Ensure only users who have booked the apartment can leave a review.
    """
    # Check if user has booked this apartment before
    booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.apartment_id == review.apartment_id,
        Booking.status.in_(["confirmed", "completed"]) # Let confirmed bookings leave reviews for now # TODO: change to completed when date checking is rigid
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You must have booked and stayed at this apartment to leave a review."
        )

    # Check if user has already reviewed this apartment
    existing_review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.apartment_id == review.apartment_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="You have already reviewed this apartment."
        )

    db_review = Review(
        apartment_id=review.apartment_id,
        user_id=current_user.id,
        rating=review.rating,
        comment=review.comment
    )
    
    try:
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating review: {str(e)}"
        )
    
    return db_review

@router.get("/apartment/{apartment_id}", response_model=List[ReviewRead])
def get_apartment_reviews(
    apartment_id: int,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Get all reviews for an apartment.
    """
    reviews = db.query(Review).filter(Review.apartment_id == apartment_id).offset(skip).limit(limit).all()
    return reviews

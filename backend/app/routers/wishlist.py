from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.wishlist import Wishlist
from app.models.user import User
from app.schemas.wishlist import WishlistCreate, WishlistRead
from app.routers.auth_enhanced import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[WishlistRead])
def get_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all wishlist items for the current user.
    """
    return db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()

@router.post("/", response_model=WishlistRead, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    wishlist: WishlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add an apartment to the user's wishlist.
    """
    db_wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.apartment_id == wishlist.apartment_id
    ).first()

    if db_wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apartment already in wishlist"
        )

    db_wishlist_item = Wishlist(
        user_id=current_user.id,
        apartment_id=wishlist.apartment_id
    )
    db.add(db_wishlist_item)
    db.commit()
    db.refresh(db_wishlist_item)
    return db_wishlist_item

@router.delete("/{apartment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_wishlist(
    apartment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove an apartment from the user's wishlist.
    """
    db_wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.apartment_id == apartment_id
    ).first()

    if not db_wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not in wishlist"
        )

    db.delete(db_wishlist_item)
    db.commit()
    return None

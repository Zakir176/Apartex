from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.blocked_date import BlockedDate
from app.models.apartment import Apartment
from app.models.user import User
from app.routers.auth_enhanced import get_current_active_user

router = APIRouter()

# ─── Pydantic Schemas (inline for simplicity) ────────────────────────
class BlockDateRangeRequest(BaseModel):
    apartment_id: int
    start_date: date
    end_date: date
    reason: str = "maintenance"  # "maintenance" | "off-market" | "personal"

class BlockedDateRead(BaseModel):
    id: int
    apartment_id: int
    blocked_date: date
    reason: str

    class Config:
        from_attributes = True

# ─── Endpoints ─────────────────────────────────────────────────────────

@router.post("/block", response_model=List[BlockedDateRead], status_code=status.HTTP_201_CREATED)
def block_date_range(
    payload: BlockDateRangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Block a range of dates for an apartment. Owner-only."""
    # Verify ownership
    apartment = db.query(Apartment).filter(Apartment.id == payload.apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    if apartment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to manage this apartment")

    if payload.start_date > payload.end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")

    created = []
    current = payload.start_date
    while current <= payload.end_date:
        # Skip if already blocked
        existing = db.query(BlockedDate).filter(
            BlockedDate.apartment_id == payload.apartment_id,
            BlockedDate.blocked_date == current
        ).first()
        if not existing:
            bd = BlockedDate(
                apartment_id=payload.apartment_id,
                blocked_date=current,
                reason=payload.reason
            )
            db.add(bd)
            created.append(bd)
        from datetime import timedelta
        current += timedelta(days=1)

    db.commit()
    for bd in created:
        db.refresh(bd)

    return created


@router.get("/{apartment_id}", response_model=List[BlockedDateRead])
def get_blocked_dates(apartment_id: int, db: Session = Depends(get_db)):
    """Get all blocked dates for an apartment. Public endpoint (used by BookingForm)."""
    return db.query(BlockedDate).filter(BlockedDate.apartment_id == apartment_id).all()


@router.delete("/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
def unblock_date(
    block_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a blocked date entry. Owner-only."""
    bd = db.query(BlockedDate).filter(BlockedDate.id == block_id).first()
    if not bd:
        raise HTTPException(status_code=404, detail="Blocked date not found")

    apartment = db.query(Apartment).filter(Apartment.id == bd.apartment_id).first()
    if not apartment or apartment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(bd)
    db.commit()
    return None

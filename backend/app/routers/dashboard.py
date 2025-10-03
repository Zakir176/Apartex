from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import OwnerDashboard, PayoutRead
from app.models.payout import Payout
from app.models.booking import Booking
from app.models.apartment import Apartment

router = APIRouter()

@router.get("/owners/{owner_id}/overview", response_model=OwnerDashboard)
def get_owner_dashboard(owner_id: int, db: Session = Depends(get_db)):
    """Get comprehensive dashboard data for property owner."""
    
    revenue_summary = DashboardService.get_revenue_summary(owner_id, db)
    booking_trends = DashboardService.get_booking_trends(owner_id, db)
    recent_bookings = DashboardService.get_recent_bookings(owner_id, db)
    top_apartments = DashboardService.get_top_performing_apartments(owner_id, db)
    
    return OwnerDashboard(
        revenue_summary=revenue_summary,
        booking_trends=booking_trends,
        recent_bookings=recent_bookings,
        top_performing_apartments=top_apartments
    )

@router.get("/owners/{owner_id}/payouts", response_model=list[PayoutRead])
def get_owner_payouts(owner_id: int, db: Session = Depends(get_db)):
    """Get payout history for owner."""
    payouts = db.query(Payout).filter(Payout.owner_id == owner_id).order_by(Payout.created_at.desc()).all()
    return payouts

@router.post("/owners/{owner_id}/payouts/request")
def request_payout(owner_id: int, db: Session = Depends(get_db)):
    """Request a payout for pending revenue."""
    # Calculate pending revenue
    pending_revenue = db.query(func.sum(Booking.total_price)).join(Apartment).filter(
        Apartment.owner_id == owner_id,
        Booking.status == "confirmed"
    ).scalar() or 0
    
    if pending_revenue <= 0:
        raise HTTPException(status_code=400, detail="No pending revenue available for payout")
    
    # Create payout record
    period_end = datetime.now().date()
    period_start = period_end - timedelta(days=30)
    
    payout = Payout(
        owner_id=owner_id,
        amount=pending_revenue,
        period_start=period_start,
        period_end=period_end,
        status="pending"
    )
    
    db.add(payout)
    db.commit()
    db.refresh(payout)
    
    return {
        "message": "Payout request submitted",
        "payout_id": payout.id,
        "amount": float(payout.amount),
        "status": payout.status
    }
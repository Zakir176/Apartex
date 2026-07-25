import csv
import io
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import OwnerDashboard, PayoutRead
from app.models.payout import Payout
from app.models.booking import Booking
from app.models.apartment import Property
from app.models.user import User
from app.routers.auth_enhanced import get_current_user

router = APIRouter()

async def verify_owner_access(current_user: User = Depends(get_current_user)):
    """Verify that the current user is an owner."""
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only property owners can access this resource"
        )
    return current_user

@router.get("/owners/{owner_id}/overview", response_model=OwnerDashboard)
def get_owner_dashboard(
    owner_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_owner_access)
):
    """Get comprehensive dashboard data for property owner."""
    # Verify the user can only access their own dashboard
    if current_user.id != owner_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own dashboard"
        )
    
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
def get_owner_payouts(
    owner_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_owner_access)
):
    """Get payout history for owner."""
    if current_user.id != owner_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own payouts"
        )
    
    payouts = db.query(Payout).filter(Payout.owner_id == owner_id).order_by(Payout.created_at.desc()).all()
    return payouts

class PayoutRequestPayload(BaseModel):
    amount: Optional[float] = None
    method: Optional[str] = "mtn"
    details: Optional[str] = None

@router.post("/owners/{owner_id}/payouts/request")
def request_payout(
    owner_id: int, 
    payload: Optional[PayoutRequestPayload] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_owner_access)
):
    """Request a payout for pending revenue."""
    if current_user.id != owner_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only request payouts for your own account"
        )
    
    # Calculate pending revenue
    pending_revenue = db.query(func.sum(Booking.total_price)).join(Property).filter(
        Property.owner_id == owner_id,
        Booking.status == "confirmed"
    ).scalar() or 0

    amount_to_pay = payload.amount if (payload and payload.amount and payload.amount > 0) else pending_revenue
    
    if amount_to_pay <= 0:
        raise HTTPException(status_code=400, detail="No pending revenue available for payout")
    
    # Create payout record
    period_end = datetime.now().date()
    period_start = period_end - timedelta(days=30)
    
    payout = Payout(
        owner_id=owner_id,
        amount=amount_to_pay,
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
        "status": payout.status,
        "method": payload.method if payload else "mtn",
        "details": payload.details if payload else ""
    }

@router.get("/owners/{owner_id}/analytics/export-csv")
def export_owner_financial_csv(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_owner_access)
):
    """Export host financial earnings and booking transactions as a CSV report."""
    if current_user.id != owner_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only export financial reports for your own account"
        )
    
    bookings = db.query(Booking).join(Property).filter(
        Property.owner_id == owner_id
    ).order_by(Booking.created_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write CSV Header
    writer.writerow([
        "Booking ID", 
        "Property Title", 
        "City", 
        "Check-In Date", 
        "Check-Out Date", 
        "Total Price ($)", 
        "Status", 
        "Created Date"
    ])
    
    # Write Rows
    for b in bookings:
        writer.writerow([
            f"#BK-{b.id}",
            b.property.title if b.property else "Property",
            b.property.city if b.property else "Zambia",
            str(b.check_in),
            str(b.check_out),
            f"{float(b.total_price):.2f}",
            b.status,
            b.created_at.strftime("%Y-%m-%d %H:%M:%S") if b.created_at else ""
        ])
    
    content = output.getvalue()
    filename = f"apartex_financial_report_owner_{owner_id}.csv"
    
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
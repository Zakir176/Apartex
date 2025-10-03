from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class RevenueSummary(BaseModel):
    total_revenue: float
    monthly_revenue: float
    pending_payouts: float
    occupancy_rate: float
    average_daily_rate: float

class BookingTrend(BaseModel):
    period: str  # "2024-01", "2024-02"
    bookings: int
    revenue: float

class OwnerDashboard(BaseModel):
    revenue_summary: RevenueSummary
    booking_trends: List[BookingTrend]
    recent_bookings: List[dict]
    top_performing_apartments: List[dict]

class PayoutCreate(BaseModel):
    owner_id: int
    amount: float
    period_start: date
    period_end: date

class PayoutRead(BaseModel):
    id: int
    owner_id: int
    amount: float
    status: str
    period_start: date
    period_end: date
    
    class Config:
        from_attributes = True
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class BookingBase(BaseModel):
    property_id: int
    check_in: date
    check_out: date
    guests: int = 1
    points_applied: Optional[int] = 0
    is_walk_in: bool = False
    payment_method: Optional[str] = None
    walk_in_guest_name: Optional[str] = None
    walk_in_guest_phone: Optional[str] = None
    created_by_owner: bool = False


BookingCreate = BookingBase
class BookingRead(BookingBase):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    status: Optional[str] = None
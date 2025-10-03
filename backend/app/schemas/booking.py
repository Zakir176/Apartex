from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class BookingBase(BaseModel):
    apartment_id: int
    check_in: date
    check_out: date
    guests: int = 1

class BookingCreate(BookingBase):
    pass

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
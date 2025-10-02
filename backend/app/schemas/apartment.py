from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApartmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: str
    city: str
    price_per_night: float
    capacity: int
    bedrooms: int
    bathrooms: int
    amenities: Optional[str] = None

class ApartmentCreate(ApartmentBase):
    pass

class ApartmentRead(ApartmentBase):
    id: int
    owner_id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
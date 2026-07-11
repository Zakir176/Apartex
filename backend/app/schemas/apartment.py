from pydantic import BaseModel
from typing import Optional, List
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
    amenities: Optional[List[str]] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

ApartmentCreate = ApartmentBase
class ApartmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    price_per_night: Optional[float] = None
    capacity: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    amenities: Optional[List[str]] = None
    image_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ApartmentRead(ApartmentBase):
    id: int
    owner_id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
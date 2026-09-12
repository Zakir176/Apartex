from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ApartmentBase(BaseModel):
    model_config = ConfigDict(extra='ignore')

    title: str
    description: Optional[str] = None
    address: Optional[str] = "Lusaka, Zambia"
    city: str = "Lusaka"
    price_per_night: float = 100.0
    capacity: int = 2
    bedrooms: int = 1
    bathrooms: int = 1
    property_type: str = "apartment"
    star_rating: Optional[int] = None
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
    property_type: Optional[str] = None
    star_rating: Optional[int] = None
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
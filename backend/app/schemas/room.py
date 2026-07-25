from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RoomBase(BaseModel):
    property_id: int
    room_type: str
    description: Optional[str] = None
    price_per_night: float
    capacity: int
    total_units: int = 1
    amenities: Optional[str] = None
    image_url: Optional[str] = None
    is_available: bool = True

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    room_type: Optional[str] = None
    description: Optional[str] = None
    price_per_night: Optional[float] = None
    capacity: Optional[int] = None
    total_units: Optional[int] = None
    amenities: Optional[str] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None

class RoomRead(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

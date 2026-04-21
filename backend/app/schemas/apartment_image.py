from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApartmentImageBase(BaseModel):
    image_url: str
    is_primary: Optional[bool] = False

class ApartmentImageCreate(ApartmentImageBase):
    apartment_id: int

class ApartmentImageRead(ApartmentImageBase):
    id: int
    apartment_id: int
    created_at: datetime

    class Config:
        from_attributes = True

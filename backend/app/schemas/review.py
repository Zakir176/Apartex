from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.review_image import ReviewImageRead

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    apartment_id: int
    image_urls: Optional[List[str]] = []

class ReviewRead(ReviewBase):
    id: int
    user_id: int
    apartment_id: int
    is_verified: bool
    created_at: datetime
    images: List[ReviewImageRead] = []
    
    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

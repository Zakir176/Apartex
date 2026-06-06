from pydantic import BaseModel
from datetime import datetime

class ReviewImageBase(BaseModel):
    image_url: str

class ReviewImageCreate(ReviewImageBase):
    pass

class ReviewImageRead(ReviewImageBase):
    id: int
    review_id: int
    created_at: datetime

    class Config:
        from_attributes = True

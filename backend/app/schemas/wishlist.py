from pydantic import BaseModel
from datetime import datetime

class WishlistBase(BaseModel):
    apartment_id: int

WishlistCreate = WishlistBase
class WishlistRead(WishlistBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """Shared user fields used across multiple schema variants."""
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "renter"

class UserCreate(UserBase):
    """Payload for creating a new user (includes plaintext password)."""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    referral_code: Optional[str] = None

class UserRead(UserBase):
    """Public representation of a user returned by the API."""
    id: int
    is_active: bool
    referral_code: Optional[str] = None
    loyalty_tier: Optional[str] = None
    loyalty_points: Optional[int] = 0

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Credentials for user login."""
    email: EmailStr
    password: str
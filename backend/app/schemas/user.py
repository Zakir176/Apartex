from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    """Shared user fields used across multiple schema variants."""
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "renter"

class UserCreate(UserBase):
    """Payload for creating a new user (includes plaintext password)."""
    password: str

class UserRead(UserBase):
    """Public representation of a user returned by the API."""
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Credentials for user login."""
    email: EmailStr
    password: str
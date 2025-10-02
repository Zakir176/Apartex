"""Authentication routes and schemas for user registration and login.

Defines minimal request/response models and two endpoints:
- POST /auth/register: create a new user
- POST /auth/login: authenticate and return a bearer token
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

# Simple request/response models (inline definitions)
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    """Request payload for user registration."""

    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    """API response model for a newly created user."""

    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login credentials payload."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT access token response body."""

    access_token: str
    token_type: str


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user.

    Args:
        user_data: Registration payload with email, password and optional full name.
        db: Database session dependency.

    Raises:
        HTTPException: 400 if the email is already registered.

    Returns:
        User: Newly created user instance (serialized by response_model).
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = hash_password(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role="renter"  # Default role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return a bearer token.

    Args:
        login_data: Email and password credentials.
        db: Database session dependency.

    Raises:
        HTTPException: 401 if credentials are invalid.

    Returns:
        dict: Access token and token type for Authorization header.
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token = create_access_token(subject=user.email)

    return {"access_token": access_token, "token_type": "bearer"}

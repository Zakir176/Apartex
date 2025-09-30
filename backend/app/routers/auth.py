from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from app.core import security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

# Register
@router.post('/register', response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    hashed = security.hash_password(user_in.password)
    user = User(email=user_in.email, full_name=user_in.full_name, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login - using OAuth2PasswordRequestForm for compat with standard flows
@router.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    token = security.create_access_token(subject=user.id)
    return {{'access_token': token, 'token_type': 'bearer'}}

# Current user
@router.get('/me', response_model=UserRead)
def me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = security.decode_token(token)
    if not payload or 'sub' not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token')
    user_id = int(payload.get('sub'))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

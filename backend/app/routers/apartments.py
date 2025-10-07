from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.apartment import Apartment
from app.schemas.apartment import ApartmentCreate, ApartmentRead
from app.routers.auth_enhanced import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ApartmentRead)
def create_apartment(
    apartment: ApartmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    if current_user.role != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can create apartments")
    db_apartment = Apartment(**apartment.dict(), owner_id=current_user.id)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment

@router.get("/", response_model=list[ApartmentRead])
def get_apartments(
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Apartment)
    if owner_id is not None:
        query = query.filter(Apartment.owner_id == owner_id)
    apartments = query.offset(skip).limit(limit).all()
    return apartments

@router.get("/{apartment_id}", response_model=ApartmentRead)
def get_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment

@router.get("/me", response_model=list[ApartmentRead])
def get_my_apartments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    if current_user.role != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can view their apartments")
    return db.query(Apartment).where(Apartment.owner_id == current_user.id).all()
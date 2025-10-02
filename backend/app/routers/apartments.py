from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.apartment import Apartment
from app.schemas.apartment import ApartmentCreate, ApartmentRead

router = APIRouter()

@router.post("/", response_model=ApartmentRead)
def create_apartment(apartment: ApartmentCreate, db: Session = Depends(get_db)):
    db_apartment = Apartment(**apartment.dict(), owner_id=1)  # Hardcode owner for now
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    return db_apartment

@router.get("/", response_model=list[ApartmentRead])
def get_apartments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    apartments = db.query(Apartment).offset(skip).limit(limit).all()
    return apartments

@router.get("/{apartment_id}", response_model=ApartmentRead)
def get_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment
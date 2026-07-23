from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.models.apartment import Property
from app.schemas.apartment import ApartmentCreate, ApartmentRead, ApartmentUpdate
from app.routers.auth_enhanced import get_current_active_user
import json

router = APIRouter()

def _prepare_apartment(apt: Property):
    if not apt: return apt
    if not apt.amenities:
        apt.amenities = []
    else:
        try:
            apt.amenities = json.loads(apt.amenities)
        except (json.JSONDecodeError, TypeError):
            # Fallback for legacy comma-strings
            apt.amenities = [s.strip() for s in apt.amenities.split(',') if s.strip()]
    return apt

@router.post("/", response_model=ApartmentRead)
def create_apartment(
    apartment: ApartmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    if current_user.role != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can create apartments")
    
    apt_data = apartment.dict()
    if isinstance(apt_data.get('amenities'), list):
        apt_data['amenities'] = json.dumps(apt_data['amenities'])
        
    db_apartment = Property(**apt_data, owner_id=current_user.id)
    db.add(db_apartment)
    db.commit()
    db.refresh(db_apartment)
    
    return _prepare_apartment(db_apartment)

@router.get("/", response_model=list[ApartmentRead])
def get_apartments(
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    capacity: Optional[int] = None,
    bedrooms: Optional[int] = None,
    amenities: Optional[List[str]] = Query(None),
    # Bounding box parameters
    min_lat: Optional[float] = None,
    max_lat: Optional[float] = None,
    min_lng: Optional[float] = None,
    max_lng: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Property)
    if owner_id is not None:
        query = query.filter(Property.owner_id == owner_id)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if min_price is not None:
        query = query.filter(Property.price_per_night >= min_price)
    if max_price is not None:
        query = query.filter(Property.price_per_night <= max_price)
    if capacity is not None:
        query = query.filter(Property.capacity >= capacity)
    if bedrooms is not None:
        query = query.filter(Property.bedrooms >= bedrooms)
    
    # Bounding box filters
    if min_lat is not None:
        query = query.filter(Property.latitude >= min_lat)
    if max_lat is not None:
        query = query.filter(Property.latitude <= max_lat)
    if min_lng is not None:
        query = query.filter(Property.longitude >= min_lng)
    if max_lng is not None:
        query = query.filter(Property.longitude <= max_lng)
    
    apartments = query.offset(skip).limit(limit).all()
    
    # Client-side filtering for amenities since they are JSON strings in DB (SQLite limitation)
    prepared = [_prepare_apartment(apt) for apt in apartments]
    
    if amenities:
        prepared = [
            apt for apt in prepared 
            if all(amenity in apt.amenities for amenity in amenities)
        ]
        
    return prepared

@router.get("/me", response_model=list[ApartmentRead])
def get_my_apartments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    if current_user.role != "owner":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can view their apartments")
    apartments = db.query(Property).where(Property.owner_id == current_user.id).all()
    return [_prepare_apartment(apt) for apt in apartments]

@router.get("/{apartment_id}", response_model=ApartmentRead)
def get_apartment(apartment_id: int, db: Session = Depends(get_db)):
    apartment = db.query(Property).filter(Property.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return _prepare_apartment(apartment)

@router.put("/{apartment_id}", response_model=ApartmentRead)
def update_apartment(
    apartment_id: int,
    update: ApartmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    apartment = db.query(Property).filter(Property.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    if current_user.role != "owner" or apartment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this apartment")
    
    update_data = update.dict(exclude_unset=True)
    if 'amenities' in update_data and isinstance(update_data['amenities'], list):
        update_data['amenities'] = json.dumps(update_data['amenities'])
        
    for field, value in update_data.items():
        setattr(apartment, field, value)
    db.add(apartment)
    db.commit()
    db.refresh(apartment)
    return _prepare_apartment(apartment)

@router.delete("/{apartment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_apartment(
    apartment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    apartment = db.query(Property).filter(Property.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    if current_user.role != "owner" or apartment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this apartment")
    db.delete(apartment)
    db.commit()
    return None
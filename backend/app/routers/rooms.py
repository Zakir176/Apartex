from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.room import Room
from app.models.apartment import Property
from app.schemas.room import RoomCreate, RoomRead, RoomUpdate
from app.routers.auth_enhanced import get_current_active_user
from app.models.user import User

router = APIRouter()

def _dump_model(model_obj, **kwargs):
    if hasattr(model_obj, "model_dump"):
        return model_obj.model_dump(**kwargs)
    return model_obj.dict(**kwargs)

# Get all rooms for a property (public)
@router.get("/property/{property_id}", response_model=List[RoomRead])
def get_rooms_for_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return db.query(Room).filter(Room.property_id == property_id, Room.is_available == True).all()

# Get all rooms for owner's property (owner only)
@router.get("/my/property/{property_id}", response_model=List[RoomRead])
def get_my_rooms(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    prop = db.query(Property).filter(Property.id == property_id, Property.owner_id == current_user.id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found or not yours")
    return db.query(Room).filter(Room.property_id == property_id).all()

# Create a room (owner only)
@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
def create_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Verify the property belongs to this owner
    prop = db.query(Property).filter(
        Property.id == room_data.property_id,
        Property.owner_id == current_user.id
    ).first()
    if not prop:
        raise HTTPException(status_code=403, detail="You do not own this property")

    room = Room(**_dump_model(room_data))
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

# Get single room (public)
@router.get("/{room_id}", response_model=RoomRead)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# Update a room (owner only)
@router.put("/{room_id}", response_model=RoomRead)
def update_room(
    room_id: int,
    room_data: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    prop = db.query(Property).filter(
        Property.id == room.property_id,
        Property.owner_id == current_user.id
    ).first()
    if not prop:
        raise HTTPException(status_code=403, detail="You do not own this property")

    for field, value in _dump_model(room_data, exclude_unset=True).items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)
    return room

# Delete a room (owner only)
@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    prop = db.query(Property).filter(
        Property.id == room.property_id,
        Property.owner_id == current_user.id
    ).first()
    if not prop:
        raise HTTPException(status_code=403, detail="You do not own this property")

    db.delete(room)
    db.commit()

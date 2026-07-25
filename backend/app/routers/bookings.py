from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List
from app.database import get_db
from app.models.booking import Booking
from app.models.apartment import Property
from app.models.user import User
from app.models.blocked_date import BlockedDate
from app.models.room import Room
from app.schemas.booking import BookingCreate, BookingRead, BookingUpdate
from app.routers.auth_enhanced import get_current_active_user

router = APIRouter()

def check_apartment_availability(apartment_id: int, check_in: date, check_out: date, db: Session) -> bool:
    """
    Check if an apartment is available for the given dates.
    Returns True if available, False if booked.
    """
    # Validate dates
    if check_in >= check_out:
        return False
    
    # Check if apartment exists and is available
    apartment = db.query(Property).filter(Property.id == apartment_id).first()
    if not apartment:
        return False
    
    if not apartment.is_available:
        return False

    # Check for overlapping bookings (only consider confirmed and completed bookings)
    overlapping_bookings = db.query(Booking).filter(
        Booking.property_id == apartment_id,
        Booking.status.in_(["confirmed", "completed"]),
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).all()
    
    if overlapping_bookings:
        return False

    # Also check owner-blocked dates
    blocked = db.query(BlockedDate).filter(
        BlockedDate.apartment_id == apartment_id,
        BlockedDate.blocked_date >= check_in,
        BlockedDate.blocked_date < check_out
    ).first()
    if blocked:
        return False
    return True

def check_room_availability(room_id: int, check_in: date, check_out: date, db: Session) -> bool:
    """
    Check if a room type has available units for the given dates.
    A room type with total_units=5 can have up to 5 overlapping bookings.
    """
    if check_in >= check_out:
        return False

    room = db.query(Room).filter(Room.id == room_id).first()
    if not room or not room.is_available:
        return False

    # Count confirmed/pending bookings for this room type in the date range
    overlapping_count = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status.in_(["confirmed", "pending"]),
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).count()

    # Available if booked count is less than total physical units
    return overlapping_count < room.total_units

def calculate_booking_price(apartment_id: int, check_in: date, check_out: date, db: Session) -> float:
    """
    Calculate total price for a booking based on apartment price and number of nights.
    """
    apartment = db.query(Property).filter(Property.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    
    nights = (check_out - check_in).days
    return nights * float(apartment.price_per_night)

def calculate_room_price(room_id: int, check_in: date, check_out: date, db: Session) -> float:
    """
    Calculate total price for a room booking.
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    nights = (check_out - check_in).days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="Check-out must be after check-in")

    return nights * float(room.price_per_night)

@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    property = db.query(Property).filter(Property.id == booking.property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    if not property.is_available:
        raise HTTPException(status_code=400, detail="Property is not available for booking")

    if booking.check_in >= booking.check_out:
        raise HTTPException(status_code=400, detail="Check-out date must be after check-in date")

    # Branch: room-based booking (hotel/lodge) vs direct property booking (apartment)
    if booking.room_id:
        room = db.query(Room).filter(
            Room.id == booking.room_id,
            Room.property_id == booking.property_id
        ).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found on this property")

        if not check_room_availability(booking.room_id, booking.check_in, booking.check_out, db):
            raise HTTPException(status_code=400, detail="Room is not available for the selected dates")

        if booking.guests > room.capacity:
            raise HTTPException(status_code=400, detail=f"Room capacity is {room.capacity} guests")

        total_price = calculate_room_price(booking.room_id, booking.check_in, booking.check_out, db)
    else:
        if not check_apartment_availability(booking.property_id, booking.check_in, booking.check_out, db):
            raise HTTPException(status_code=400, detail="Property is not available for the selected dates")

        if booking.guests > property.capacity:
            raise HTTPException(status_code=400, detail=f"Property can only accommodate {property.capacity} guests")

        total_price = calculate_booking_price(booking.property_id, booking.check_in, booking.check_out, db)

    if booking.guests < 1:
        raise HTTPException(status_code=400, detail="Number of guests must be at least 1")

    # Apply loyalty points discount
    if booking.points_applied and booking.points_applied > 0:
        if current_user.loyalty_points < booking.points_applied:
            raise HTTPException(status_code=400, detail="Not enough loyalty points")
        discount = booking.points_applied / 100.0
        if discount > total_price:
            discount = total_price
            booking.points_applied = int(total_price * 100)
        current_user.loyalty_points -= booking.points_applied
        total_price -= discount

    db_booking = Booking(
        property_id=booking.property_id,
        room_id=booking.room_id,
        user_id=current_user.id,
        check_in=booking.check_in,
        check_out=booking.check_out,
        guests=booking.guests,
        total_price=total_price,
        status="confirmed",
        is_walk_in=False,
        payment_method=booking.payment_method,
        walk_in_guest_name=None,
        walk_in_guest_phone=None,
        created_by_owner=False,
    )

    try:
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating booking: {str(e)}")

    return db_booking

@router.post("/walk-in", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_walk_in_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Owner-only endpoint. Records a walk-in or phone booking for a guest
    who does not have an Apartex account. Blocks availability immediately.
    """
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Only property owners can record walk-in bookings")

    if not booking.walk_in_guest_name or not booking.walk_in_guest_name.strip():
        raise HTTPException(status_code=400, detail="walk_in_guest_name is required for walk-in bookings")

    if not booking.payment_method:
        raise HTTPException(status_code=400, detail="payment_method is required for walk-in bookings")

    if booking.payment_method not in ["cash", "mobile_money", "card", "bank_transfer"]:
        raise HTTPException(status_code=400, detail="payment_method must be one of: cash, mobile_money, card, bank_transfer")

    if booking.check_in >= booking.check_out:
        raise HTTPException(status_code=400, detail="Check-out date must be after check-in date")

    property = db.query(Property).filter(
        Property.id == booking.property_id,
        Property.owner_id == current_user.id
    ).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found or you do not own it")

    # Availability check — same logic as regular booking
    if booking.room_id:
        room = db.query(Room).filter(
            Room.id == booking.room_id,
            Room.property_id == booking.property_id
        ).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found on this property")

        if not check_room_availability(booking.room_id, booking.check_in, booking.check_out, db):
            raise HTTPException(status_code=400, detail="Room is not available for the selected dates")

        total_price = calculate_room_price(booking.room_id, booking.check_in, booking.check_out, db)
    else:
        if not check_apartment_availability(booking.property_id, booking.check_in, booking.check_out, db):
            raise HTTPException(status_code=400, detail="Property is not available for the selected dates")

        total_price = calculate_booking_price(booking.property_id, booking.check_in, booking.check_out, db)

    db_booking = Booking(
        property_id=booking.property_id,
        room_id=booking.room_id,
        user_id=None,
        check_in=booking.check_in,
        check_out=booking.check_out,
        guests=booking.guests,
        total_price=total_price,
        status="confirmed",
        is_walk_in=True,
        payment_method=booking.payment_method,
        walk_in_guest_name=booking.walk_in_guest_name.strip(),
        walk_in_guest_phone=booking.walk_in_guest_phone,
        created_by_owner=True,
    )

    try:
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating walk-in booking: {str(e)}")

    return db_booking

@router.get("/", response_model=List[BookingRead])
def get_bookings(
    skip: int = 0, 
    limit: int = 100, 
    property_id: int = None,
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get bookings. Owners see bookings for their properties; renters see only their own.
    Admins can optionally filter by property_id or user_id.
    """
    query = db.query(Booking)

    if current_user.role == "owner":
        # Owners can only see bookings for properties they own
        query = query.join(Property, Booking.property_id == Property.id).filter(
            Property.owner_id == current_user.id
        )
        if property_id is not None:
            query = query.filter(Booking.property_id == property_id)
    else:
        # Renters can only see their own bookings
        query = query.filter(Booking.user_id == current_user.id)
        if user_id is not None and user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own bookings."
            )
    
    bookings = query.offset(skip).limit(limit).all()
    return bookings

@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific booking. Only the renter who made it or the apartment owner can view it.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    apartment = db.query(Property).filter(Property.id == booking.property_id).first()
    is_renter = booking.user_id == current_user.id
    is_apartment_owner = apartment and apartment.owner_id == current_user.id

    if not is_renter and not is_apartment_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this booking."
        )

    return booking

@router.put("/{booking_id}", response_model=BookingRead)
def update_booking(
    booking_id: int, 
    booking_update: BookingUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a booking. Only the renter who made it or the apartment owner can update it.
    """
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    apartment = db.query(Property).filter(Property.id == db_booking.property_id).first()
    is_renter = db_booking.user_id == current_user.id
    is_apartment_owner = apartment and apartment.owner_id == current_user.id

    if not is_renter and not is_apartment_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this booking."
        )
    
    # Update fields
    update_data = booking_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_booking, field, value)
    
    try:
        db.commit()
        db.refresh(db_booking)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating booking: {str(e)}"
        )
    
    return db_booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete (cancel) a booking. Only the renter who made it can delete it.
    """
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this booking."
        )
    
    try:
        db.delete(booking)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Error deleting booking: {str(e)}"
        )
    
    return None

@router.get("/apartment/{apartment_id}/availability")
def check_availability(
    apartment_id: int,
    check_in: date,
    check_out: date,
    db: Session = Depends(get_db)
):
    """
    Check availability for specific dates for an apartment.
    """
    # Check if apartment exists
    apartment = db.query(Property).filter(Property.id == apartment_id).first()
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    
    # Check availability
    is_available = check_apartment_availability(apartment_id, check_in, check_out, db)
    
    # Calculate price if available
    price = None
    if is_available:
        try:
            price = calculate_booking_price(apartment_id, check_in, check_out, db)
        except:
            price = "Error calculating price"
    
    return {
        "apartment_id": apartment_id,
        "check_in": check_in,
        "check_out": check_out,
        "is_available": is_available,
        "total_price": price,
        "apartment_details": {
            "title": apartment.title,
            "price_per_night": float(apartment.price_per_night),
            "capacity": apartment.capacity
        }
    }

@router.get("/room/{room_id}/availability")
def check_room_availability_endpoint(
    room_id: int,
    check_in: date,
    check_out: date,
    db: Session = Depends(get_db)
):
    """
    Check availability for a specific room type for given dates.
    Returns available unit count.
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    overlapping_count = db.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.status.in_(["confirmed", "pending"]),
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).count()

    units_available = room.total_units - overlapping_count
    is_available = units_available > 0

    nights = (check_out - check_in).days
    total_price = nights * float(room.price_per_night) if is_available and nights > 0 else None

    return {
        "room_id": room_id,
        "room_type": room.room_type,
        "check_in": check_in,
        "check_out": check_out,
        "is_available": is_available,
        "units_available": max(0, units_available),
        "total_units": room.total_units,
        "total_price": total_price,
        "price_per_night": float(room.price_per_night),
    }

@router.get("/user/{user_id}/bookings", response_model=List[BookingRead])
def get_user_bookings(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all bookings for a specific user.
    """
    # Enforce authorization: only allow the user themselves or an admin to access these bookings
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view these bookings."
        )

    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return bookings

@router.get("/owner/{owner_id}/bookings", response_model=List[BookingRead])
def get_owner_bookings(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all bookings for apartments owned by the specified owner.
    Only the owner (or admin in future) can access their bookings.
    """
    if current_user.id != owner_id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only access your own bookings")
    bookings = db.query(Booking).join(Property, Booking.property_id == Property.id).filter(
        Property.owner_id == owner_id
    ).all()
    return bookings

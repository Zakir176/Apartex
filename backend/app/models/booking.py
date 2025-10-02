from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Booking(Base):
    """Reservation linking a renter to an apartment for a date range."""
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"))
    renter_id = Column(Integer, ForeignKey("users.id"))
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled, completed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    apartment = relationship("Apartment", back_populates="bookings")
    renter = relationship("User", back_populates="bookings")
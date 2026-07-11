from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Apartment(Base):
    __tablename__ = "apartments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    address = Column(String(300), nullable=False)
    city = Column(String(100), nullable=False)
    price_per_night = Column(Numeric(10, 2), nullable=False)
    capacity = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    amenities = Column(Text)  # JSON string of amenities
    image_url = Column(String(500))  # Optional primary image URL
    is_available = Column(Boolean, default=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Simple foreign key for now
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    wishlists = relationship("Wishlist", back_populates="apartment")
    reviews = relationship("Review", back_populates="apartment", cascade="all, delete-orphan")
    apartment_images = relationship("ApartmentImage", back_populates="apartment", cascade="all, delete-orphan")
    blocked_dates = relationship("BlockedDate", back_populates="apartment", cascade="all, delete-orphan")
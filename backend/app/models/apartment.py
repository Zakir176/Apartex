from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric
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
    is_available = Column(Boolean, default=True)
    owner_id = Column(Integer, nullable=False)  # Simple foreign key for now
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
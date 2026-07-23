from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BlockedDate(Base):
    __tablename__ = "blocked_dates"

    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    blocked_date = Column(Date, nullable=False)

    reason = Column(String, default="maintenance")  # "maintenance" | "off-market" | "personal"

    apartment = relationship("Property", back_populates="blocked_dates")


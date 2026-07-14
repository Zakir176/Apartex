from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from sqlalchemy import inspect, Column, String
from app.models import user, apartment, booking, loyalty, payout, wishlist, review, apartment_image, blocked_date
from app.routers import apartments, bookings, loyalty as loyalty_router, dashboard, auth_enhanced, wishlist as wishlist_router, reviews, availability
from app.routers import uploads

import logging

logger = logging.getLogger(__name__)

# Create all tables securely
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.error("Failed to create database tables", exc_info=True)
    raise

app = FastAPI(title="Apartex API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "https://apartex.vercel.app"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Include routers with /api prefix
app.include_router(auth_enhanced.router, prefix="/api/auth-enhanced", tags=["authentication-enhanced"])
app.include_router(apartments.router, prefix="/api/apartments", tags=["apartments"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])
app.include_router(loyalty_router.router, prefix="/api/loyalty", tags=["loyalty"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(uploads.router, prefix="/api/upload", tags=["uploads"])
app.include_router(wishlist_router.router, prefix="/api/wishlist", tags=["wishlist"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(availability.router, prefix="/api/availability", tags=["availability"])
# Static files for uploads (ONLY point to uploads directory for security)
import os
uploads_dir = os.path.join(os.getcwd(), "uploads")
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/")
def read_root():
    return {"message": "Apartex API is running!"}
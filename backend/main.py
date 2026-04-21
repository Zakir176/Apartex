from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from sqlalchemy import inspect, Column, String
from app.models import user, apartment, booking, loyalty, payout, wishlist, review, apartment_image, blocked_date
from app.routers import apartments, bookings, loyalty as loyalty_router, dashboard, auth_enhanced, wishlist as wishlist_router, reviews, availability
from app.routers import uploads

# Create all tables
Base.metadata.create_all(bind=engine)

# Lightweight migration: ensure apartments.image_url exists
try:
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('apartments')]
    if 'image_url' not in columns:
        with engine.connect() as conn:
            # Use SQLAlchemy 2.x compatible execution for raw SQL
            conn.exec_driver_sql("ALTER TABLE apartments ADD COLUMN image_url VARCHAR(500)")
except Exception as e:
    # Non-fatal: log-like print so devs can see it
    print(f"[startup] apartments.image_url migration check failed or unnecessary: {e}")

app = FastAPI(title="Apartex API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "https://apartex.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
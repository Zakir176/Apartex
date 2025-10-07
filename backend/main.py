from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from sqlalchemy import inspect, Column, String
from app.models import user, apartment, booking, loyalty, payout
from app.routers import auth, apartments, bookings, loyalty as loyalty_router, dashboard, auth_enhanced
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
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:8080",  # Vue CLI default port  
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "https://apartex.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(auth_enhanced.router, prefix="/auth-enhanced", tags=["authentication-enhanced"])
app.include_router(apartments.router, prefix="/apartments", tags=["apartments"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(loyalty_router.router, prefix="/loyalty", tags=["loyalty"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(uploads.router, prefix="/upload", tags=["uploads"])

# Static files for uploads
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def read_root():
    return {"message": "Apartex API is running!"}
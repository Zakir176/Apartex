from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user, apartment, booking, loyalty, payout
from app.routers import auth, apartments, bookings, loyalty as loyalty_router, dashboard, auth_enhanced

# Create all tables
Base.metadata.create_all(bind=engine)

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

@app.get("/")
def read_root():
    return {"message": "Apartex API is running!"}
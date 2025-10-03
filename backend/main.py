from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, apartment, booking  # Add booking
from app.routers import auth, apartments, bookings  # Add bookings

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Apartex API", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(apartments.router, prefix="/apartments", tags=["apartments"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])  # Add this line

@app.get("/")
def read_root():
    return {"message": "Apartex API is running!"}
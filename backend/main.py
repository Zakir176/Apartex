from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, apartment  # Import models to create tables
from app.routers import auth, apartments

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Apartex API", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(apartments.router, prefix="/apartments", tags=["apartments"])

@app.get("/")
def read_root():
    return {"message": "Apartex API is running!"}
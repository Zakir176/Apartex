"""Database configuration and session utilities.

Creates the SQLAlchemy engine, session factory, declarative base,
and a generator function for request-scoped sessions (FastAPI dependency).
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./apartex.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Yield a database session and ensure it is closed after use.

    Designed for use as a FastAPI dependency to provide a per-request session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
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

def init_db():
    """Ensure all models are created and SQLite column migrations are applied."""
    from sqlalchemy import inspect, text
    import app.models  # Ensure all models are registered
    Base.metadata.create_all(bind=engine)
    try:
        inspector = inspect(engine)
        if "bookings" in inspector.get_table_names():
            cols = [c["name"] for c in inspector.get_columns("bookings")]
            if "room_id" not in cols:
                with engine.connect() as conn:
                    conn.execute(text("ALTER TABLE bookings ADD COLUMN room_id INTEGER REFERENCES rooms(id)"))
                    conn.commit()
    except Exception:
        pass

def get_db():
    """Yield a database session and ensure it is closed after use.

    Designed for use as a FastAPI dependency to provide a per-request session.
    """
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
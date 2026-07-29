# Backend — Developer Guide

Overview
- The backend implements the API, business logic, and data persistence.

Run locally

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Copy .env.example to .env and set required environment variables
uvicorn app.main:app --reload --port 8000
```

Environment variables
- If the backend uses a .env file, list important variables here (DATABASE_URL, SECRET_KEY, etc.).

Database & migrations
- Document how to initialize the database and run migrations (e.g., Alembic, Django migrations, or custom scripts).

Testing

```bash
pytest
```

Logging & Debugging
- Tail logs when running in Docker: `docker-compose logs -f backend`

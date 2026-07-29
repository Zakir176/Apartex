# Getting Started

This guide helps you run Apartex locally using Docker or local development environments.

Prerequisites
- Git
- Docker & docker-compose (optional, recommended for full-stack local testing)
- Node 16+ / npm or yarn (for frontend development)
- Python 3.8+ (if backend is Python)

Clone repository

```bash
git clone https://github.com/Zakir176/Apartex.git
cd Apartex
```

Option A — Run with Docker Compose (recommended if docker-compose.yml exists)

```bash
docker-compose up --build
```

- Frontend should be available at http://localhost:3000 (confirm in docker-compose.yml)
- Backend API should be available at http://localhost:8000 (or configured port)

Option B — Run services locally

Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Set environment variables by copying .env.example -> .env if present
uvicorn app.main:app --reload --port 8000
```

Frontend

```bash
cd frontend
npm install
# Create .env.local with API base URL if needed
npm start
```

First request example
- See docs/examples/quick_example.py for a sample request to the API.

Next steps
- Read docs/usage.md for how to interact with the API and UI
- Read docs/backend.md and docs/frontend.md for developer setup

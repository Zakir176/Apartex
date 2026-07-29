# Architecture

High-level components
- Frontend — React (or other) UI
- Backend — API server handling requests and data storage
- Database — persistent store (Postgres, SQLite, etc.)
- Optional: worker queue, cache, or external services

Data flow (example)
1. User interacts with frontend UI
2. Frontend calls backend API
3. Backend reads/writes data to the database and returns responses

Deployment
- For development: docker-compose
- For production: containerize services and use an orchestration platform (Kubernetes, ECS, etc.)

Diagrams
- Add architecture diagrams (SVG/PNG) here if desired.

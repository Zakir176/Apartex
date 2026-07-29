# Troubleshooting & FAQ

Common issues

1. docker-compose fails to build
   - Make sure Docker is running and you have sufficient resources.
   - Check for missing environment variables.

2. Backend errors
   - Check backend logs and ensure database is migrated/initialized.

3. Frontend cannot reach backend
   - Verify API base URL settings in frontend environment variables.

FAQ
- Where is the database stored?
  - Explain whether a local SQLite or a remote Postgres instance is used.
- How to run tests?
  - `pytest` for backend, `npm test` for frontend.

If you need help, open an issue including logs and steps to reproduce.

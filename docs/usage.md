# Usage

This page shows common usage patterns: API, CLI (if present), and web UI examples.

API (example)
- Base URL: http://localhost:8000 (adjust if different)

Sample endpoint (replace with real endpoints from your backend):

POST /api/predict or /api/items

Request JSON:

```json
{
  "example_field": "value",
  "meta": { "user": "demo" }
}
```

Response JSON:

```json
{
  "result": "ok",
  "data": {}
}
```

Note: Start the backend and visit /docs or /openapi (if FastAPI) to inspect actual endpoints.

Python usage (example)
- See docs/examples/quick_example.py for a full script that posts JSON to the backend and prints the response.

Web UI
- The frontend provides the main UI for interacting with Apartex. Common pages include listings, item detail, and admin pages.

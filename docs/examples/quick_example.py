# Quick example: call backend API (Python)

Save as docs/examples/quick_example.py and run with Python 3.8+ after installing requests

```python
import requests
import json

BASE_URL = "http://localhost:8000"  # adjust if different
PATH = "/api/items"                 # replace with real endpoint

payload = {
    "example_field": "value",
    "meta": {"user": "demo"}
}

try:
    resp = requests.post(BASE_URL + PATH, json=payload, timeout=15)
    resp.raise_for_status()
    print(json.dumps(resp.json(), indent=2))
except Exception as e:
    print("Request failed:", e)
```

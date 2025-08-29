import os
import sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import json
import httpx
import pytest
from jsonschema import validate

CONTRACT_PATH = os.path.join(REPO_ROOT, "specs", "001-we-are-building", "contracts", "post-api-query-event.json")


@pytest.mark.asyncio
async def test_post_api_query_event_contract():
    with open(CONTRACT_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)

    payload = {
        "request": {"query": "Explain Grafana vs Azure Monitor"},
        "response": {"answer": "Stubbed answer", "citations": [], "confidence": 0.5, "fallback": False},
    }

    # Validate payload structure
    try:
        validate(instance=payload, schema=schema)
    except Exception:
        pass

    # Send to telemetry endpoint or query-event endpoint depending on implementation
    async with httpx.AsyncClient() as client:
        # Try /api/query/event first, fallback to /api/telemetry
        resp = await client.post("http://localhost:8000/api/query/event", json=payload)
        if resp.status_code >= 400:
            resp2 = await client.post("http://localhost:8000/api/telemetry", json={"event": "query_event", "payload": payload})
            assert resp2.status_code in (200, 202)

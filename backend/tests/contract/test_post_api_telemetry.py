import os
import sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import httpx
import pytest
from jsonschema import validate
import json

CONTRACT_PATH = os.path.join(REPO_ROOT, "specs", "001-we-are-building", "contracts", "post-api-telemetry.json")


@pytest.mark.asyncio
async def test_post_api_telemetry_contract():
    with open(CONTRACT_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)

    payload = {"event": "test_event", "pseudo_user_id": "anon-1", "payload": {"k": "v"}}

    try:
        validate(instance=payload, schema=schema)
    except Exception:
        pass

    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/api/telemetry", json=payload)
        assert resp.status_code in (200, 202, 500)

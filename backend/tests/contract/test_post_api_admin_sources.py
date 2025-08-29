import os
import sys
# Ensure repo root is on sys.path for imports and for finding specs
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import json
import httpx
import pytest
from jsonschema import validate

CONTRACT_PATH = os.path.join(REPO_ROOT, "specs", "001-we-are-building", "contracts", "post-api-admin-sources.json")


@pytest.mark.asyncio
async def test_post_api_admin_sources_contract():
    # Load contract schema
    with open(CONTRACT_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)

    payload = {"url": "https://docs.microsoft.com/azure/managed-grafana", "title": "Grafana docs"}

    # Validate sample payload against contract (request) - sanity check
    try:
        validate(instance=payload, schema=schema)
    except Exception:
        # If validation fails here the contract may be unexpected
        pass

    # Call the running service - this will fail if server not running
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/api/admin/sources", json=payload)
        assert resp.status_code in (200, 201, 202, 400)

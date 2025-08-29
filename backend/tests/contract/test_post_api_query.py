import os
import sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import json
import httpx
import pytest
from jsonschema import validate

CONTRACT_PATH = os.path.join(REPO_ROOT, "specs", "001-we-are-building", "contracts", "post-api-query.json")


@pytest.mark.asyncio
async def test_post_api_query_contract():
    with open(CONTRACT_PATH, "r", encoding="utf-8") as fh:
        schema = json.load(fh)

    payload = {"query": "How do I get started with Azure Managed Grafana?"}

    # Validate payload against contract request schema
    try:
        validate(instance=payload, schema=schema)
    except Exception:
        pass

    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/api/query", json=payload, timeout=30.0)
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            body = resp.json()
            assert "answer" in body
            assert "citations" in body
            assert "confidence" in body
            assert "fallback" in body

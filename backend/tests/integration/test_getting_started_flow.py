import os
import sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import httpx
import pytest


@pytest.mark.asyncio
async def test_getting_started_flow():
    payload = {"query": "How do I get started with Azure Managed Grafana?"}
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/api/query", json=payload, timeout=30.0)
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            body = resp.json()
            assert isinstance(body.get("answer"), str)

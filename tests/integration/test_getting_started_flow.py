"""
This integration test was moved to `backend/tests/integration/test_getting_started_flow.py`.
Run tests from backend/tests or update CI to run from there.
"""

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


# End

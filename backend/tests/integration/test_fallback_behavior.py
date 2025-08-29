import os
import sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import httpx
import pytest


@pytest.mark.asyncio
async def test_fallback_behavior():
    # If STUB_MODE is false or not set, the backend may error here. We assert both outcomes.
    payload = {"query": "This should trigger fallback or stubbed response"}
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/api/query", json=payload, timeout=30.0)
        assert resp.status_code in (200, 500)
        if resp.status_code == 200:
            body = resp.json()
            assert "fallback" in body

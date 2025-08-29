import os
import sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import pytest
from backend.src.services.sources_service import add_source, list_sources, clear_sources


@pytest.mark.asyncio
async def test_sources_service_add_and_list():
    await clear_sources()
    payload = type("P", (), {"url": "https://example.com", "title": "x", "priority": 50})()
    created = await add_source(payload)
    assert "id" in created
    sources = await list_sources()
    assert isinstance(sources, list)
    assert len(sources) >= 1

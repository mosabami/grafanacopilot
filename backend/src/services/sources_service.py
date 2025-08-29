"""Minimal in-memory Admin Sources service for prototype.

This service provides add/list operations and is a placeholder for a DB-backed
implementation (to be added later in `backend/src/db.py`).
"""

from typing import Dict, List, Any
from uuid import uuid4

_SOURCES: List[Dict] = []


async def add_source(payload) -> Dict[str, Any]:
    """Add a source using DB CRUD helpers when available; otherwise fall back to in-memory."""
    url = getattr(payload, "url", None) or (payload.get("url") if isinstance(payload, dict) else None)
    title = getattr(payload, "title", None) or (payload.get("title") if isinstance(payload, dict) else None)
    priority = getattr(payload, "priority", None) or (payload.get("priority") if isinstance(payload, dict) else 100)

    try:
        from backend.src.db.crud import create_source

        return await create_source(url, title=title, priority=priority)
    except Exception:
        # Fallback to in-memory store
        source = {
            "id": str(uuid4()),
            "url": url,
            "title": title,
            "priority": priority or 100,
            "last_indexed": None,
            "active": True,
        }
        _SOURCES.append(source)
        return source


async def list_sources() -> List[Dict[str, Any]]:
    try:
        from backend.src.db.crud import list_sources_db

        return await list_sources_db()
    except Exception:
        return list(_SOURCES)


async def clear_sources() -> None:
    # Try DB path first
    try:
        from backend.src.db.crud import list_sources_db, delete_source

        rows = await list_sources_db(limit=1000)
        for r in rows:
            try:
                await delete_source(r.get("id"))
            except Exception:
                pass
        # Also clear in-memory
        _SOURCES.clear()
        return
    except Exception:
        _SOURCES.clear()
        return

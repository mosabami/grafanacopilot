"""Telemetry service: record usage events to in-memory store or DB (prototype).

This implementation records events in an in-memory list for local dev. Later,
this should persist to Postgres using `backend/src/db.py`.
"""

from typing import Dict, Any

_USAGE_EVENTS = []


async def record_event(event: Dict[str, Any]) -> None:
    try:
        from backend.src.db.crud import create_usage_event

        await create_usage_event(event)
        return
    except Exception:
        # Fallback to in-memory
        pass

    import uuid, datetime

    e = dict(event)
    e.setdefault("id", str(uuid.uuid4()))
    e.setdefault("event_time", datetime.datetime.utcnow().isoformat())
    _USAGE_EVENTS.append(e)


async def list_events() -> list:
    try:
        from backend.src.db.crud import list_usage_events

        return await list_usage_events()
    except Exception:
        return list(_USAGE_EVENTS)


async def clear_events() -> None:
    try:
        from backend.src.db.crud import list_usage_events, delete_usage_event

        rows = await list_usage_events(limit=1000)
        for r in rows:
            try:
                await delete_usage_event(r.get("id"))
            except Exception:
                pass
        _USAGE_EVENTS.clear()
        return
    except Exception:
        _USAGE_EVENTS.clear()
        return

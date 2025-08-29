"""Minimal CRUD helpers using the async SQLAlchemy session provided by `backend.src.db`.

These functions are intentionally tiny and call `get_sessionmaker()` lazily to avoid
import-time cycles. They return native Python dicts for convenience in the prototype.
"""

from typing import Optional, List, Dict, Any


async def create_source(url: str, title: Optional[str] = None, priority: int = 100) -> Dict[str, Any]:
    from backend.src.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    from backend.src.db.models import Source as ORMSource

    async with SessionLocal() as session:
        src = ORMSource(url=url, title=title, priority=priority)
        session.add(src)
        await session.commit()
        await session.refresh(src)
        return {
            "id": str(src.id),
            "url": src.url,
            "title": src.title,
            "priority": src.priority,
            "last_indexed": None,
            "active": src.active,
        }


async def get_source_by_id(source_id: str) -> Optional[Dict[str, Any]]:
    from backend.src.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    import uuid

    try:
        pk = uuid.UUID(source_id)
    except Exception:
        pk = source_id

    from backend.src.db.models import Source as ORMSource

    async with SessionLocal() as session:
        src = await session.get(ORMSource, pk)
        if src is None:
            return None
        return {
            "id": str(src.id),
            "url": src.url,
            "title": src.title,
            "priority": src.priority,
            "last_indexed": src.last_indexed.isoformat() if src.last_indexed else None,
            "active": src.active,
        }


async def list_sources_db(limit: int = 100) -> List[Dict[str, Any]]:
    from backend.src.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    from backend.src.db.models import Source as ORMSource
    from sqlalchemy import select

    async with SessionLocal() as session:
        result = await session.execute(select(ORMSource).order_by(ORMSource.priority).limit(limit))
        rows = result.scalars().all()
        return [
            {
                "id": str(r.id),
                "url": r.url,
                "title": r.title,
                "priority": r.priority,
                "last_indexed": r.last_indexed.isoformat() if r.last_indexed else None,
                "active": r.active,
            }
            for r in rows
        ]


async def update_source(source_id: str, **updates) -> Optional[Dict[str, Any]]:
    from backend.src.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    import uuid

    try:
        pk = uuid.UUID(source_id)
    except Exception:
        pk = source_id

    from backend.src.db.models import Source as ORMSource

    async with SessionLocal() as session:
        src = await session.get(ORMSource, pk)
        if not src:
            return None
        for k, v in updates.items():
            if hasattr(src, k):
                setattr(src, k, v)
        await session.commit()
        await session.refresh(src)
        return {
            "id": str(src.id),
            "url": src.url,
            "title": src.title,
            "priority": src.priority,
            "last_indexed": src.last_indexed.isoformat() if src.last_indexed else None,
            "active": src.active,
        }


async def delete_source(source_id: str) -> bool:
    from backend.src.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    import uuid
    from sqlalchemy import delete
    from backend.src.db.models import Source as ORMSource

    try:
        pk = uuid.UUID(source_id)
    except Exception:
        pk = source_id

    async with SessionLocal() as session:
        await session.execute(delete(ORMSource).where(ORMSource.id == pk))
        await session.commit()
        return True


# Usage events CRUD
async def create_usage_event(event: dict) -> Dict[str, Any]:
    from backend.src.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    from backend.src.db.models import UsageEvent as ORMUsageEvent

    async with SessionLocal() as session:
        ue = ORMUsageEvent(
            pseudo_user_id=event.get("pseudo_user_id"),
            event_type=event.get("event", "event"),
            query_hash=event.get("query_hash"),
            confidence=event.get("confidence"),
            citations=event.get("citations"),
            anchors=event.get("anchors"),
            metadata=event.get("payload") or event.get("metadata"),
        )
        session.add(ue)
        await session.commit()
        await session.refresh(ue)
        return {
            "id": str(ue.id),
            "pseudo_user_id": ue.pseudo_user_id,
            "event_time": ue.event_time.isoformat() if ue.event_time else None,
            "event_type": ue.event_type,
            "metadata": ue.metadata,
        }


async def list_usage_events(limit: int = 100) -> List[Dict[str, Any]]:
    from backend.src.db import get_sessionmaker

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    from backend.src.db.models import UsageEvent as ORMUsageEvent
    from sqlalchemy import select

    async with SessionLocal() as session:
        result = await session.execute(select(ORMUsageEvent).order_by(ORMUsageEvent.event_time.desc()).limit(limit))
        rows = result.scalars().all()
        return [
            {
                "id": str(r.id),
                "pseudo_user_id": r.pseudo_user_id,
                "event_time": r.event_time.isoformat() if r.event_time else None,
                "event_type": r.event_type,
                "metadata": r.metadata,
            }
            for r in rows
        ]


async def delete_usage_event(event_id: str) -> bool:
    from backend.src.db import get_sessionmaker
    import uuid
    from sqlalchemy import delete
    from backend.src.db.models import UsageEvent as ORMUsageEvent

    SessionLocal = get_sessionmaker()
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured for DB-backed persistence")

    try:
        pk = uuid.UUID(event_id)
    except Exception:
        pk = event_id

    async with SessionLocal() as session:
        await session.execute(delete(ORMUsageEvent).where(ORMUsageEvent.id == pk))
        await session.commit()
        return True

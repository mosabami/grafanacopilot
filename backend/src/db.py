"""DB helper: simple helpers for connecting to Postgres using SQLAlchemy.

This module exposes the async engine/session factory and a convenience `create_all()`
so the prototype can create tables on startup.
"""

import os
from typing import AsyncGenerator

try:
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import text
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
except Exception:
    # SQLAlchemy may not be installed in the minimal analysis environment
    create_async_engine = None  # type: ignore
    AsyncSession = None  # type: ignore
    sessionmaker = None  # type: ignore
    text = None  # type: ignore


# DATABASE_URL = "postgresql+asyncpg://postgres:correctpassword@localhost:5432/postgres"
DATABASE_URL = os.environ.get("DATABASE_URL")
_async_engine = None
_async_sessionmaker = None


def init_db_engine() -> None:
    global _async_engine, _async_sessionmaker
    if _async_engine is not None:
        return
    if not DATABASE_URL:
        return
    _async_engine = create_async_engine(DATABASE_URL, future=True, echo=False)
    _async_sessionmaker = sessionmaker(_async_engine, expire_on_commit=False, class_=AsyncSession)


def get_engine():
    init_db_engine()
    return _async_engine


def get_sessionmaker():
    init_db_engine()
    return _async_sessionmaker


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an AsyncSession for use with 'async with' or as a FastAPI dependency."""
    SessionLocal = get_sessionmaker()
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL not set; DB helpers are not available")
    async with SessionLocal() as session:
        yield session


async def create_all() -> dict:
    """Create DB tables from SQLAlchemy models and return per-table status.

    Returns a dict: {table_name: "created" | "already_existed" | "unknown"}
    """
    engine = get_engine()
    if engine is None:
        raise RuntimeError("DATABASE_URL not configured")
    # Import models lazily to avoid import cycles
    

    status = {}
    async with engine.begin() as conn:
        # Ensure pgcrypto exists for gen_random_uuid()
        try:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
        except Exception:
            # extension may not be supported on some providers; ignore extension errors
            pass

        # Check existence before creating
        preexist = {}
        for name in Base.metadata.tables.keys():
            try:
                val = await conn.scalar(text(f"SELECT to_regclass('public.{name}')"))
                preexist[name] = bool(val)
            except Exception:
                preexist[name] = False

        # Create missing tables (idempotent)
        await conn.run_sync(Base.metadata.create_all)

        # Check existence after creation and compute status
        for name in Base.metadata.tables.keys():
            try:
                val = await conn.scalar(text(f"SELECT to_regclass('public.{name}')"))
                post = bool(val)
            except Exception:
                post = False
            if preexist.get(name):
                status[name] = "already_existed" if post else "unknown"
            else:
                status[name] = "created" if post else "unknown"

    return status


# Expose CRUD helpers from the separate module for compatibility
try:
    # import * so external callers that used db.create_source continue to work
    from backend.src.db.crud import (
        create_source,
        get_source_by_id,
        list_sources_db,
        update_source,
        delete_source,
        create_usage_event,
        list_usage_events,
    )
except Exception:
    # Not a fatal error for local dev — if crud is not available, callers will see errors when calling
    pass

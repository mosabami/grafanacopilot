#!/usr/bin/env python3
"""Initialize Postgres schema for the prototype.

This script uses `asyncpg` to create the `sources` and `usage_events` tables if they
do not exist. It reads DATABASE_URL from env.
"""

import os
import asyncio


async def main():
    # Try SQLAlchemy-based creation first
    try:
        from src.db import create_all

        await create_all()
        print("DB initialized via SQLAlchemy metadata.create_all()")
        return
    except Exception as e:
        print("SQLAlchemy create_all() unavailable or failed; falling back to asyncpg: %s" % e)

    # dsn = "postgresql+asyncpg://postgres:correctpassword@localhost:5432/postgres"
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        print("DATABASE_URL not set — skipping DB initialization")
        return
    try:
        import asyncpg
    except Exception:
        print("asyncpg is not installed; install with 'pip install asyncpg'")
        return

    SQL_SOURCES = """
    CREATE TABLE IF NOT EXISTS sources (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      url TEXT NOT NULL,
      title TEXT,
      priority INTEGER DEFAULT 100,
      last_indexed TIMESTAMPTZ,
      active BOOLEAN DEFAULT true
    );
    """

    SQL_USAGE_EVENTS = """
    CREATE TABLE IF NOT EXISTS usage_events (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      pseudo_user_id TEXT,
      event_time TIMESTAMPTZ DEFAULT now(),
      event_type TEXT NOT NULL,
      query_hash TEXT,
      confidence REAL,
      citations JSONB,
      anchors JSONB,
      metadata JSONB
    );
    """

    conn = await asyncpg.connect(dsn)
    await conn.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    await conn.execute(SQL_SOURCES)
    await conn.execute(SQL_USAGE_EVENTS)
    await conn.close()
    print("DB initialized via asyncpg")


if __name__ == "__main__":
    asyncio.run(main())

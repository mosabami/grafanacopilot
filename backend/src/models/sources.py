"""Pydantic model for `sources` (prototype).

This mirrors the `data-model.md` entry for sources.
"""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import datetime


class Source(BaseModel):
    id: Optional[str] = None
    url: str
    title: Optional[str] = None
    priority: int = 100
    last_indexed: Optional[datetime.datetime] = None
    active: bool = True


# Small helper to serialise DB rows (if present)
def serialize_source(row: dict) -> dict:
    return {
        "id": row.get("id"),
        "url": row.get("url"),
        "title": row.get("title"),
        "priority": row.get("priority", 100),
        "last_indexed": row.get("last_indexed"),
        "active": row.get("active", True),
    }

"""Pydantic model for `usage_events` (prototype).

See `data-model.md` for fields and structure.
"""

from pydantic import BaseModel
from typing import Optional, List, Any
import datetime


class UsageEvent(BaseModel):
    id: Optional[str] = None
    pseudo_user_id: Optional[str] = None
    event_time: Optional[datetime.datetime] = None
    event_type: str
    query_hash: Optional[str] = None
    confidence: Optional[float] = None
    citations: Optional[List[dict]] = None
    anchors: Optional[List[str]] = None
    metadata: Optional[dict] = None


def serialize_usage_event(row: dict) -> dict:
    return {**row}

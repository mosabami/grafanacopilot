"""SQLAlchemy ORM models for the prototype.

- `Source` table mirrors `data-model.md` `sources`
- `UsageEvent` table mirrors `data-model.md` `usage_events`

These are the canonical DB models used by Alembic and SQLAlchemy.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func, text

Base = declarative_base()


class Source(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    url = Column(Text, nullable=False)
    title = Column(Text, nullable=True)
    priority = Column(Integer, nullable=False, default=100)
    last_indexed = Column(DateTime(timezone=True), nullable=True)
    active = Column(Boolean, nullable=False, default=True)


class UsageEvent(Base):
    __tablename__ = "usage_events"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    pseudo_user_id = Column(Text, nullable=True)
    event_time = Column(DateTime(timezone=True), server_default=func.now())
    event_type = Column(Text, nullable=False)
    query_hash = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    citations = Column(JSONB, nullable=True)
    anchors = Column(JSONB, nullable=True)
    metadata = Column(JSONB, nullable=True)

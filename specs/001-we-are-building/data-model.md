# Data Model

This document lists the minimal data model for the prototype. The model focuses on capturing usage events and admin-managed sources. No PII should be persisted.

## Entities

### sources
- Description: Admin-configurable list of documentation URLs used to prioritize retrieval.
- Fields:
  - id: UUID (primary key)
  - url: TEXT (documentation URL)
  - title: TEXT (optional display title)
  - priority: INTEGER (lower = higher priority, default 100)
  - last_indexed: TIMESTAMPTZ (nullable)
  - active: BOOLEAN (default TRUE)

### usage_events
- Description: Minimal telemetry for each Copilot interaction. Does not contain raw PII.
- Fields:
  - id: UUID (primary key)
  - pseudo_user_id: TEXT (pseudonymous identifier)
  - event_time: TIMESTAMPTZ
  - event_type: TEXT ("query" | "response" | "feedback" | "click")
  - query_hash: TEXT (optional hashed query value, not raw query)
  - confidence: REAL (0..1)
  - citations: JSONB (list of citation objects)
  - anchors: JSONB (list of anchors linked to page sections)
  - metadata: JSONB (any additional non-PII metadata)

## Sample SQL (Postgres)

Create `sources` table:

```sql
CREATE TABLE IF NOT EXISTS sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  url TEXT NOT NULL,
  title TEXT,
  priority INTEGER DEFAULT 100,
  last_indexed TIMESTAMPTZ,
  active BOOLEAN DEFAULT true
);
```

Create `usage_events` table:

```sql
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
```

Notes:
- Keep `query_hash` or other query representations scrubbed/hashed to avoid storing PII.
- For local prototype, `gen_random_uuid()` requires the `pgcrypto` extension. Alternatively set UUID values programmatically from the app.

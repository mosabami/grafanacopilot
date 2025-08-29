# Implementation Plan: Azure Managed Grafana Copilot (Simple Prototype)

**Branch**: `001-we-are-building` | **Date**: 2025-08-28  
**Goal**: Deliver a functional prototype website + Copilot in a few hours (local/dev). Prioritize simplicity and a working demo over full test/gate coverage.


## Scope (MVP)

- Complete marketing site prototype (landing/hero, concise value propositions, Getting Started CTA, FAQ, customer logos/use cases) plus the Copilot sidebar integrated into the site (not a standalone chatbot page).
- The Copilot UI is embedded as a resizable, non-overlapping sidebar with greeting/expectations, scrollable history, copy buttons, and anchor linking to page sections.
- Backend FastAPI endpoints to support both streaming and non-streaming responses (see API Contracts). Streaming responses must follow the structure and content rules in `specs/001-we-are-building/spec.md` (citations, anchors, fallbacks).
- Admin-configurable list of Grafana doc URLs (in-memory for prototype; persisted in Postgres if time).
- Telemetry: emit to Application Insights using provided connection string and log to console for local debugging; persist minimal usage_events to Postgres when DATABASE_URL set, otherwise use an in-memory buffer.
- Support STUB_MODE=true when Foundry/MCP keys are not configured. In STUB_MODE the system returns canned, spec-compliant responses and logs how it would have retrieved/grounded content.


## Architecture (simple)

- frontend/ — React + TypeScript (Vite). Copilot UI component lives here.
- backend/ — Python + FastAPI. Endpoints: /api/query, /api/admin/sources, /api/telemetry.
- db/ — Postgres (docker-compose for local dev).
- LLM: Azure AI Foundry Agent (call or stub).
- Retrieval: Azure MCP server (or local stub for prototype).
- Hosting later: Azure Container Apps (not required for initial prototype).


## Minimal Integration Flow (prototype)

1. Frontend POST /api/query (or open stream to /api/query/stream) { query, pseudo_user_id? }

2. Backend flow (sync or streaming):
   - Check STUB_MODE or presence of AI_FOUNDRY_API_KEY & MCP config; if stub -> build canned response using prioritized sources list;
   - Otherwise call MCP retrieval (prioritize admin sources), assemble prompt compliant with `specs/001-we-are-building/spec.md` (include requested citation policy), then call Azure Foundry in streaming mode to produce tokens + citation chunks;
   - Stream tokens to the frontend as they arrive (SSE / chunked HTTP) including inline citations and anchor directives; after stream finishes include final confidence and citation summary.

3. Emit telemetry incrementally (stream start/partial/complete) to Application Insights and print to console; persist a minimal usage_event when DATABASE_URL is set (otherwise push event to in-memory store for short-term debugging).


## FastAPI API Contracts (MVP) — add streaming

- POST /api/query (non-streaming)
  - Request: { "query": string, "pseudo_user_id"?: string }
  - Response: { "answer": string, "citations": [...], "confidence": number, "fallback": boolean }

- POST /api/query/stream (streaming; SSE or chunked)
  - Client: opens a streaming request (SSE or HTTP chunked) including the same JSON payload; server streams partial tokens + citation markers and a final JSON summary event with confidence and citation array.

- POST /api/admin/sources (prototype: API key authentication optional)
  - Request: { "url": string }

- POST /api/telemetry
  - Request: { "event": string, "pseudo_user_id"?: string, "payload": object }


## Configuration (.env files)

Place a `.env` file at the root of each container (backend/.env and frontend/.env). Required keys (prototype):

````text
AI_FOUNDRY_ENDPOINT=...
AI_FOUNDRY_API_KEY=...
AI_FOUNDRY_PROJECT=...
APPINSIGHTS_CONNECTION_STRING=...
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ADMIN_API_KEY=secret-api-key
STUB_MODE=true
````

- Backend must read `STUB_MODE` and fall back to the stub behavior when true or when AI keys are missing.
- Frontend .env should include only public-safe keys or flags (e.g., STUB_MODE) and the backend URL.


## Telemetry & persistence behavior

- Emit telemetry to Application Insights using APPINSIGHTS_CONNECTION_STRING when provided. Also print telemetry JSON to console for local debugging.
- Persist minimal usage_events to Postgres when DATABASE_URL is present. If DATABASE_URL is missing, store events in an in-memory list (app.state.in_memory_usage_events) for debugging and eventual flush if DB becomes available.


## Local dev quick-start (docker-compose + env_file)

- Provide a docker-compose.yml with services: frontend, backend, postgres. Use env_file to load `backend/.env` and `frontend/.env` so local config is trivial.

Example docker-compose snippet (expand as needed):

````yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: grafanacopilot
    ports:
      - '5432:5432'
    volumes:
      - pgdata:/var/lib/postgresql/data

  backend:
    build: ./backend
    env_file:
      - ./backend/.env
    depends_on:
      - postgres
    ports:
      - '8000:8000'

  frontend:
    build: ./frontend
    env_file:
      - ./frontend/.env
    ports:
      - '3000:3000'

volumes:
  pgdata:
````

- Dockerfiles already target Linux-compatible bases (python:3.11-slim, node:20-alpine) so images are suitable for later Azure Container Apps deployment.


## Stub mode requirements

- When STUB_MODE=true or AI_FOUNDRY_API_KEY is absent, the backend should:
  - Use canned responses that are compliant with `specs/001-we-are-building/spec.md` (include citations and anchors where appropriate).
  - Log that it is operating in stub mode and the reason (missing keys or explicit flag) via console and App Insights.


## Minimal code note (persistence & stub mode)

- Ensure the example FastAPI handler checks `STUB_MODE` and `DATABASE_URL` environment variables and chooses the appropriate path (stub vs real call; in-memory vs DB persist).


## Deliverable (unchanged)

- Working local demo that runs via docker-compose, supports streaming or non-streaming queries, obeys spec-driven response format, supports stub mode, logs telemetry to console and App Insights (if configured), persists to Postgres when configured, and uses `.env` files for trivial configuration.

# Quickstart — Prototype (local)

This quickstart shows how to run the simplified prototype locally using docker-compose. It assumes Docker and docker-compose (or Docker Desktop) are installed.

## 1) Create .env files

Create `backend/.env` with the following keys (example values):

```
AI_FOUNDRY_ENDPOINT=https://foundry.example
AI_FOUNDRY_API_KEY=
AI_FOUNDRY_PROJECT=managed-grafana-proj
APPINSIGHTS_CONNECTION_STRING=
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/grafanacopilot
ADMIN_API_KEY=changeme
STUB_MODE=true
```

Create `frontend/.env` with minimal settings:

```
VITE_API_BASE_URL=http://localhost:8000
STUB_MODE=true
```

## 2) Start Postgres and services

A minimal `docker-compose.yml` is in the plan. Start services:

```bash
docker-compose up --build -d
```

This will:
- Start Postgres
- Build and start backend (exposes port 8000)
- Build and start frontend (exposes port 3000)

## 3) Initialize DB (optional)

If you want to create the sample tables, run:

```bash
# using psql (local) — adjust host/port per docker-compose
PGPASSWORD=postgres psql -h localhost -U postgres -d grafanacopilot -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
PGPASSWORD=postgres psql -h localhost -U postgres -d grafanacopilot -c "CREATE TABLE IF NOT EXISTS sources (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), url TEXT NOT NULL, title TEXT, priority INTEGER DEFAULT 100, last_indexed TIMESTAMPTZ, active BOOLEAN DEFAULT true);"
PGPASSWORD=postgres psql -h localhost -U postgres -d grafanacopilot -c "CREATE TABLE IF NOT EXISTS usage_events (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), pseudo_user_id TEXT, event_time TIMESTAMPTZ DEFAULT now(), event_type TEXT NOT NULL, query_hash TEXT, confidence REAL, citations JSONB, anchors JSONB, metadata JSONB);"
```

## 4) Add admin sources (prototype)

Add a URL to the admin sources list (replace ADMIN_API_KEY value):

```bash
curl -X POST http://localhost:8000/api/admin/sources \
  -H "Content-Type: application/json" \
  -H "x-api-key: changeme" \
  -d '{"url":"https://docs.microsoft.com/azure/managed-grafana"}'
```

## 5) Test a query (non-streaming)

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"How do I get started with Azure Managed Grafana?"}'
```

## 7) Debug telemetry & DB

- Console: backend prints telemetry JSON to stdout for local debugging.
- App Insights: configure APPINSIGHTS_CONNECTION_STRING in backend/.env to send telemetry.
- Postgres: verify rows in `usage_events`.

## 8) Turn off stub mode

Set `STUB_MODE=false` and configure `AI_FOUNDRY_API_KEY` and MCP endpoint in `backend/.env` and restart the backend to test the real integration.

## Notes
- For prototype, simple API key is used for admin endpoints. In production replace with Azure AD and RBAC.
- The quickstart focuses on the local demo. Deployment to Azure Container Apps requires creating images and following the production deployment flow (CI/CD) described in the plan.

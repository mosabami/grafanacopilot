Backend quickstart (prototype)

This is the minimal backend for the Grafana Copilot prototype.

Quick steps (local dev):

1. Create env file: `backend/.env` with the following keys (example):

```
AI_FOUNDRY_ENDPOINT=
AI_FOUNDRY_API_KEY=
AI_FOUNDRY_PROJECT=
APPINSIGHTS_CONNECTION_STRING=
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/grafanacopilot
ADMIN_API_KEY=changeme
STUB_MODE=true
```

2. Install dependencies:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
```

3. Initialize DB (optional):

```bash
python backend/scripts/init_db.py
```

4. Run backend locally:

```bash
uvicorn backend.src.app:app --host 0.0.0.0 --port 8000 --reload
```

5. Run tests (once dependencies installed):

```bash
pytest -q
```

Notes
- STUB_MODE=true will cause the `/api/query` endpoint to return canned responses, useful for development without AI keys.
- This backend is intentionally minimal; extend services and replace in-memory stores with Postgres-backed implementations in `backend/src/db.py` when ready.

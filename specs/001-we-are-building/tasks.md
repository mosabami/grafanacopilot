# Tasks: Azure Managed Grafana Marketing Copilot & Page Redesign (001-we-are-building)

**Feature directory (from check script)**: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building

**Available design docs**:
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/plan.md
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/research.md
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/data-model.md
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/quickstart.md
- Contracts: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/contracts/

---

Notes:
- This tasks list follows the TDD-first approach in `plan.md` and the Task Generation rules from the template.
- Paths below are absolute (WSL-style, /mnt/c/...). Adjust if running from Windows native shell.
- Filing strategy: backend code will live under `backend/` (so quickstart examples map directly). Tests are under `tests/` at repo root.

## Task ID format
- Each task has an ID T###, optional `[P]` when the task can be executed in parallel (different files / no dependencies).
- Dependency notes describe blocking/dependent tasks.

---

## Phase 3.1 — Setup

T001  Create `backend/` skeleton and minimal FastAPI app (sequential)
- Path(s):
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/app.py
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/__init__.py
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/start.sh
- Description: Create a minimal Python FastAPI app that exposes a placeholder route at `/api/health` and mounts /api endpoints from a `backend/src/api.py` module. App must listen on port 8000 (default in quickstart). Include a README note referencing `STUB_MODE=true` for local runs.
- Files to create (LLM action): create `backend/src/app.py` with a FastAPI app skeleton and instructions to run `uvicorn backend.src.app:app --host 0.0.0.0 --port 8000`.
- Dependencies: None (pure scaffolding). Must be completed before tests that call endpoints (T004-T007).

T002  Create `backend/requirements.txt` and development tools (sequential)
- Path: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/requirements.txt
- Description: Add pinned packages for prototype.
  - Required pins (candidate):
    - azure-ai-agents==1.1.0
    - fastapi>=0.95
    - uvicorn[standard]>=0.20
    - pydantic>=1.10
    - pytest>=7.0
    - pytest-asyncio
    - httpx>=0.24
    - asyncpg>=0.27
    - jsonschema
    - python-dotenv
    - alembic (optional for migrations)
  - Add dev tools: black, ruff, isort (optional)
- LLM Action: Create the file with the above pins and include a brief comment explaining usage. Do not install packages now (developer or CI will run `pip install -r backend/requirements.txt`).
- Dependencies: T001

T003  Configure linting & formatting (parallel)
- Path(s):
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/pyproject.toml
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/.pre-commit-config.yaml (optional)
- Description: Add configuration for black/isort/ruff to keep code style consistent. This is independent — mark [P].
- Dependencies: None

---

## Phase 3.2 — Tests First (TDD) ⚠️ MUST COMPLETE BEFORE IMPLEMENTATION

Rules applied:
- Each contract file → one contract test file [P]
- Each user story/acceptance scenario → integration test [P]
- Tests must be written to fail (they exercise endpoints that are not implemented yet)

T004 [P] Contract test — POST /api/admin/sources
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/contract/test_post_api_admin_sources.py
- Contract source: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/contracts/post-api-admin-sources.json
- Description: Create a pytest test that:
  1. Loads the JSON Schema from the absolute contract path.
  2. Builds a valid sample request payload (e.g. {"url": "https://docs.microsoft.com/..."}).
  3. Uses `jsonschema.validate()` to assert the payload matches the contract request schema (sanity check).
  4. Sends an HTTP POST to `http://localhost:8000/api/admin/sources` using `httpx`.
  5. If the service responds, validate the response body shape against the **response** expectations (if contract defines one). If the service is missing, the test will fail (expected initially).
- Dependency notes: Depends on T001/T002 to create server and install deps before being runnable locally. Must be created before implementation of `/api/admin/sources`.

T005 [P] Contract test — POST /api/query (request/response)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/contract/test_post_api_query.py
- Contract source: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/contracts/post-api-query.json
- Description: Same pattern as T004: load schema, post a sample `{"query": "How do I get started with Azure Managed Grafana?"}`, assert response matches structure: answer (string), citations (array), confidence (number 0..1), fallback (boolean).
- Dependency notes: Depends on T001/T002.

T006 [P] Contract test — POST /api/query event schema
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/contract/test_post_api_query_event.py
- Contract source: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/contracts/post-api-query-event.json
- Description: Test POST to `http://localhost:8000/api/query/event` or include the event payload validation if the project plans to use internal recording. Validate payload format (request + response) as per schema.
- Dependency notes: Depends on T001/T002.

T007 [P] Contract test — POST /api/telemetry
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/contract/test_post_api_telemetry.py
- Contract source: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/contracts/post-api-telemetry.json
- Description: Send a sample telemetry event and validate accepted payload.
- Dependency notes: Depends on T001/T002.

T008 [P] Integration test(s) — Quickstart scenarios (non-streaming)
- Files:
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/integration/test_quickstart_query.py
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/integration/test_getting_started_flow.py
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/integration/test_fallback_behavior.py
- Description: Translate the acceptance scenarios from `spec.md` / `quickstart.md` into integration tests that run against `http://localhost:8000`:
  - Comparative question -> POST `/api/query` and assert `citations` and `answer` exist.
  - Getting started question -> POST `/api/query` and assert a short 3-step answer or presence of a link.
  - Fallback -> Simulate low confidence scenario (if config `STUB_MODE=true`, create a stubbed response with `fallback=true`).
- Dependency notes: Depends on contract tests (T004-T007) being in place and T001/T002 to make tests runnable.

---

## Phase 3.3 — Core Implementation (ONLY after tests are created and failing)

Guideline: Implement in this order: models → DB connection → services → endpoints. Endpoints will be placed in the same file `backend/src/api.py` (sequential endpoint tasks, no [P]).

T009 [P] Model: `sources` (Pydantic + DB model)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/models/sources.py
- Source: data-model: `sources` entity in `/specs/001-we-are-building/data-model.md`
- Description: Create a Pydantic model for request/response validation and a SQLAlchemy ORM (or minimal asyncpg table create helper) model for persistence. Fields: id (UUID), url (TEXT), title (TEXT), priority (INTEGER default 100), last_indexed (TIMESTAMPTZ), active (BOOLEAN default true).
- Test expectation: Unit tests (T019) will exercise serialization & validation.
- Dependency notes: Must be created prior to services that operate on `sources`.

T010 [P] Model: `usage_events` (Pydantic + DB model)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/models/usage_events.py
- Source: data-model: `usage_events` entity in `/specs/001-we-are-building/data-model.md`
- Description: Create Pydantic model and DB model matching fields: id UUID, pseudo_user_id, event_time TIMESTAMPTZ, event_type, query_hash, confidence, citations (JSON), anchors (JSON), metadata (JSON).
- Dependency notes: Required for telemetry endpoint/service.

T011  DB integration: create connection helper & migrations (sequential)
- Files:
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/db.py
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/alembic/ (optional)
- Description:
  - Implement an async DB connection helper that reads `DATABASE_URL` from env (per quickstart). Use SQLAlchemy AsyncEngine or `asyncpg` directly. Provide `get_db()` dependency for FastAPI endpoints.
  - Provide a small script `backend/scripts/init_db.py` that runs `CREATE TABLE` statements from `data-model.md` sample SQL (so QA can easily run local DB init using quickstart commands).
- Dependency notes: Services using DB must depend on this task.

T012  Service: Admin Sources service (sequential)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/services/sources_service.py
- Description: Implement functions:
  - add_source(db, url, title=None, priority=100) → inserts into `sources`
  - list_sources(db) → returns active sources ordered by priority
- Dependency notes: Depends on T009 and T011.

T013  Endpoint: Implement POST /api/admin/sources (sequential, same API file)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/api.py
- Description:
  - Add route `POST /api/admin/sources` to validate input via Pydantic, authenticate via `x-api-key` header (ADMIN_API_KEY from env, quickstart example), and call `sources_service.add_source` to persist.
  - Return created resource (JSON) or HTTP 401 if API key missing/invalid.
- Dependency notes: Depends on T009/T011/T012. This task shares `backend/src/api.py` with other endpoints, so it must be implemented sequentially (no [P]).

T014  Service: Query service calling Azure AI Foundry (sequential)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/services/query_service.py
- Description: Implement a synchronous call to the Responses API via `azure-ai-agents==1.1.0` using `AI_FOUNDRY_API_KEY` from env. For prototype:
  - Support `STUB_MODE` env var: when `STUB_MODE=true`, return canned responses for tests.
  - Accept query text + optional page_context and return object with `answer`, `citations` (list of {url, anchor, snippet}), `confidence` (float), `fallback` (bool).
- Dependency notes: Depends on T011 for telemetry DB access if telemetry is recorded by query flow.

T015  Endpoint: Implement POST /api/query (sequential)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/api.py (same file as T013)
- Description:
  - Add route that accepts the request contract (see `/specs/.../contracts/post-api-query.json`).
  - Calls `query_service.query(...)` and returns the response object.
  - Log telemetry (send event to usage_events via telemetry service) and return a standard response shape matching contract.
- Dependency notes: Depends on T014 and T011/T010 models.

T016  Endpoint: Implement POST /api/telemetry (sequential)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/api.py
- Description:
  - Endpoint to accept telemetry events per contract `/contracts/post-api-telemetry.json` and persist into `usage_events`.
  - Validate payload and return 202 or 200 on success.
- Dependency notes: Depends on T010/T011.

---

## Phase 3.4 — Integration & Observability

T017 [P] Observability: Add structured logging and App Insights (optional exporter)
- Files:
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/observability.py
- Description:
  - Configure Python logging with structured JSON output.
  - Add optional OpenTelemetry export to Application Insights (`azure-monitor-opentelemetry-exporter`) when `APPINSIGHTS_CONNECTION_STRING` exists. Provide a simple toggle to enable/disable.
- Dependency notes: Independent of API endpoints – mark [P].

T018 [P] Health check & middleware
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/api.py (add middleware imports)
- Description: Add `GET /api/health` (if not present), CORS middleware (allow origin from quickstart), and request/response logging middleware.
- Dependency notes: Minor change; adjust if conflicts arise. If API file already contains health, skip.

T019 [P] Integration: Add script for initializing DB for local dev (quickstart)
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/scripts/init_db.py
- Description: A simple script that connects to DATABASE_URL and creates `sources` and `usage_events` tables (use SQL from `data-model.md`). Mark [P] — safe to run in parallel with observability tasks.
- Dependency notes: Requires T011 to be implemented or can be standalone script that uses asyncpg.

---

## Phase 3.5 — Polish

T020 [P] Unit tests for models and services
- Files:
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/unit/test_models.py
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/unit/test_services.py
- Description: Add unit tests for Pydantic model validation and for service helpers using in-memory or stubbed DB connections. These tests should be marked [P] (different files) and must pass after implementation.
- Dependency notes: Depends on T009/T010/T012/T014.

T021  Performance & smoke tests (sequential or parallel)
- File(s): `/mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/perf/test_latency.py` (optional)
- Description: Add a small load test (e.g., 10 concurrent requests to `/api/query` with `STUB_MODE=true`) and measure average latency. Test not required to be exhaustive but should be runnable locally.
- Dependency notes: After endpoints implemented.

T022 [P] Documentation updates & quickstart verification
- Files:
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/specs/001-we-are-building/tasks.md (this file)
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/README.md (update to mention backend quickstart)
  - /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/README.md (quickstart for backend)
- Description: Update quickstart instructions to pin `STUB_MODE` usage and to include how to run tests locally. Mark [P].
- Dependency notes: After core implementation & tests passing.

T023  CI: Add GitHub Actions workflow for tests
- File: /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/.github/workflows/ci.yml
- Description: Create a minimal workflow that installs python, installs `backend/requirements.txt`, runs `pytest -q`. This protects future PRs.
- Dependency notes: After test files (T004-T008 & unit tests) exist.

---

## Task ordering & dependencies (summary)
- Setup: T001 -> T002 -> T003
- Tests: T004-T008 (contract + quickstart integration) created after T001/T002 (these tests must fail first)
- Models: T009-T010 must be created before DB & services
- DB helper (T011) is required before services persist data; create early in core stage
- Services: T012 (sources) and T014 (query) depend on models & DB
- Endpoints: T013-T016 implemented sequentially in the shared API file `/backend/src/api.py`
- Integration & Observability: T017-T019 after endpoints exist, unless they are safe to add earlier (they are mostly additive) — many are [P].
- Polish & CI: T020-T023 after implementation and initial test pass.

---

## Parallel execution examples

1) Create contract tests in parallel (these are independent files)

Shell example (WSL bash):

```bash
pytest -q tests/contract/test_post_api_admin_sources.py &
pytest -q tests/contract/test_post_api_query.py &
pytest -q tests/contract/test_post_api_query_event.py &
pytest -q tests/contract/test_post_api_telemetry.py &
wait
```

2) Create model files in parallel (different files)

```bash
# Run code generation helpers or LLM tasks in parallel (example):
( ./scripts/create-model.sh "sources" & )
( ./scripts/create-model.sh "usage_events" & )
wait
```

3) Task agent example (LLM-runner pseudo-command):
- To instruct the agent to create multiple independent tasks at once (example syntax — replace with your agent runner if different):

```
# PSEUDO-COMMAND
task-agent run --id T004 & task-agent run --id T005 & task-agent run --id T006 & wait
```

Notes:
- Use the `[P]` marker to identify tasks that are safe to run concurrently (independent files). If tasks modify the same file (e.g., `/backend/src/api.py`), do NOT run them in parallel.

---

## File map (where to expect work / file targets)
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/app.py  # FastAPI entrypoint
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/api.py  # All endpoints (sequential implement)
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/models/*.py
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/services/*.py
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/db.py
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/backend/src/observability.py
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/contract/*.py
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/integration/*.py
- /mnt/c/Users/aayodeji/git/grafana/grafanacopilot/tests/unit/*.py

---

## Validation checklist (what to verify after generation)
- [ ] All contract files produce a corresponding `tests/contract/test_*.py` (T004-T007)
- [ ] All entities in `data-model.md` have a model task (T009-T010)
- [ ] Quickstart scenarios have integration tests (T008)
- [ ] Tests are present and to be run under `pytest` (they should fail initially)
- [ ] Tasks referencing the same file are not marked [P]
- [ ] Tasks include exact absolute file paths

---

If you want, I will now:
1) Create these test skeletons and model skeletons (write the files in the repo) so you can run `pytest` and observe failing tests, or
2) Create only the `tasks.md` (this file) and wait for your permission before writing any code files.

Choose (1) or (2).

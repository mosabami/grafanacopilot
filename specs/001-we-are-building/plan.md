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
   - Check STUB_MODE or presence of PROJECT_ENDPOINT & MCP config; if stub -> build canned response using prioritized sources list;
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
PROJECT_ENDPOINT=...  # Foundry project endpoint, e.g. https://<resource>.services.ai.azure.com/api/projects/<project-name>
AI_FOUNDRY_PROJECT=...  # optional model/project/deployment identifier
APPINSIGHTS_CONNECTION_STRING=...
DATABASE_URL=postgresql://user:pass@host:5432/dbname
ADMIN_API_KEY=secret-api-key
STUB_MODE=true
````

- Backend must read `STUB_MODE` and fall back to the stub behavior when true or when project-level credentials / endpoint are missing.
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

- When STUB_MODE=true or PROJECT_ENDPOINT is missing, the backend should:
  - Use canned responses that are compliant with `specs/001-we-are-building/spec.md` (include citations and anchors where appropriate).
  - Log that it is operating in stub mode and the reason (missing keys or explicit flag) via console and App Insights.


## Minimal code note (persistence & stub mode)

- Ensure the example FastAPI handler checks `STUB_MODE` and `DATABASE_URL` environment variables and chooses the appropriate path (stub vs real call; in-memory vs DB persist).


## Deliverable (unchanged)

- Working local demo that runs via docker-compose, supports streaming or non-streaming queries, obeys spec-driven response format, supports stub mode, logs telemetry to console and App Insights (if configured), persists to Postgres when configured, and uses `.env` files for trivial configuration.


## AI Foundry Agent — Retrieval & Implementation (prototype)

- Authentication (important): For this prototype we will use DefaultAzureCredential only. The agent will authenticate using managed identity or developer credentials via `DefaultAzureCredential()` and the project-level APIs (no API-key-based auth is used).

  - Required environment variables (backend/.env):
    - PROJECT_ENDPOINT — the full project endpoint for your Foundry project (for example, `https://<resource>.services.ai.azure.com/api/projects/<project-name>`).
    - AI_FOUNDRY_PROJECT (optional) — project or deployment identifier, if needed by the endpoint.

  - Implementation note: instantiate the project-level client with `DefaultAzureCredential` and the project endpoint. Example (prototype):

    ```python
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    import os

    project = AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv('PROJECT_ENDPOINT')
    )

    # Retrieve an existing agent (the agent is already created in AI Foundry for the prototype)
    # Example: get agent by id (or name if supported). Replace AGENT_ID with your agent identifier.
    agent = project.agents.get_agent(os.getenv('FOUNDARY_AGENT_ID', 'asst_yqZHPJUIFMjXNS693gcP7z6K'))

    # Example run flow (create thread, post a message, create and process run)
    from azure.ai.agents.models import ListSortOrder

    thread = project.agents.threads.create()
    project.agents.messages.create(thread_id=thread.id, role='user', content='Why should I use this service?')

    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    # After the run completes, list messages and extract assistant text
    if run.status == 'failed':
        raise RuntimeError(f'Agent run failed: {run.last_error}')
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    # parse messages to extract assistant content / citations
    ```

  - If the SDK or project-level APIs are not available or misconfigured, the prototype will raise a clear configuration error. For local development use `STUB_MODE=true` to get canned responses.

- Retrieval strategy — use the MCP server (mslearn) as the primary source:
  - The agent will be configured with an MCP tool (server_label `mslearn`, server_url `https://learn.microsoft.com/api/mcp`) so it can query the Microsoft Learn (mslearn) MCP server for documentation.
  - For each incoming query, the agent should attempt a prioritized search of the MCP server and return grounded results. Prioritization rules:
    - If the user explicitly names a service (e.g., "Grafana", "Azure Monitor"), narrow the MCP search to that service.
    - If the user does *not* specify a service, assume they refer to "Azure Managed Grafana" and prime the agent to prioritize that documentation first.
    - If Azure Managed Grafana docs do not produce a satisfactory answer, broaden the MCP search to additional Microsoft Learn docs available on the server.

  - Tool configuration:
    - Configure the agent in Azure AI Foundry (project) to include MCP retrieval (server_label `mslearn`, server_url `https://learn.microsoft.com/api/mcp`) or equivalent retrieval tooling. Set any prototype approval mode to `never` to allow automatic retrieval. The backend should not attempt to instantiate or manage Foundry retrieval tool classes; instead the agent should be pre-configured in Foundry to perform retrieval during runs.
    - The backend's responsibility is to forward the incoming request's message as the `content` field of a message to the agent (for example: `project.agents.messages.create(thread_id=thread.id, role='user', content=user_query)`), call `project.agents.runs.create_and_process(...)`, and parse the run/messages for final answer and citations.

  - Results & snippets:
    - The agent should return citation references (URLs and short snippets) taken from the MCP results or from the page text returned by the MCP tool. If the MCP run includes structured tool_calls or step outputs, parse those for citations and snippets.

  - Fetching page content: only attempt direct HTTP fetches for expanded snippets when an env flag `FETCH_LINK_CONTENT=true` is set; otherwise prefer using MCP-provided text and metadata.

- Prompt & grounding policy (prototype):
  - If the user's query does not explicitly name a service, treat the query as referring to Azure Managed Grafana and prioritize mslearn results for that product before returning results from other docs.
  - The prompt should instruct the agent to:
    1. Use only the provided sources unless explicitly asked to fetch or mention external resources.
    2. Provide inline citations using a numbered syntax [1], [2], ... where numbers correspond to the provided source list.
    3. Provide a short answer, then a citations array that lists objects {url, anchor, snippet}. If the agent cannot find a grounded answer, set `fallback=true` and explain briefly.
  - Include a short system-level instruction in the prompt template that enforces the citation policy and output shape (JSON-like summary) so the post-processing step can extract the final `answer`, `citations`, `confidence`, and `fallback` fields.

- Agent invocation & parsing:
  - For non-streaming queries: call the Agents SDK (preferred) or REST endpoint with the prompt + context; parse the returned content to find the final answer text and any citations the agent embedded. If the SDK returns structured outputs (e.g., tool calls / run steps), prefer reading tool call outputs and run conclusions.
  - Heuristics to extract citations:
    - Look for inline markers like [1], [2] in the text and correlate to the provided source list.
    - If the agent includes explicit URL mentions, include them as citations as well.
  - Build the final response shape: {answer: string, citations: [{url, anchor?, snippet?}], confidence: float, fallback: bool}.

- Telemetry and observability:
  - Emit a telemetry event per query with: query text (or hashed), pseudo_user_id (if provided), STUB_MODE flag, number_of_candidates, selected_sources (urls), and final fallback flag.
  - Log the same payload to console for local debugging and to App Insights when `APPINSIGHTS_CONNECTION_STRING` exists.

- Implementation steps (high-level):
   1. Configure retrieval in Foundry (no backend mcp_tool_helper required):
      - Configure the existing agent in Azure AI Foundry to include MCP retrieval (server_label `mslearn`) or equivalent discovery tools. Do not attempt to instantiate/connect an MCP tool from the backend; the agent should be pre-configured in the Foundry project to perform any MCP searches during its runs.
      - The backend will simply create a thread, post the user's message (setting `content` to the incoming request `query`), call `runs.create_and_process(...)`, and parse messages/run_steps for the answer and citations.
   2. Update `backend/src/services/query_service.py`:
      - When STUB_MODE=true, return canned response (existing behavior).
      - When STUB_MODE=false:
        a. Build an agent prompt that includes a short system instruction and the user query. If the user did not specify a target product/service, add an instruction to assume the query concerns "Azure Managed Grafana" and prioritize mslearn docs for that product.
        b. Instantiate the project-level client using `DefaultAzureCredential()` and the project endpoint. Example:
+
+```python
+from azure.ai.projects import AIProjectClient
+from azure.identity import DefaultAzureCredential
+import os
+
+project = AIProjectClient(credential=DefaultAzureCredential(), endpoint=os.getenv('PROJECT_ENDPOINT'))
+agent = project.agents.get_agent(os.getenv('FOUNDARY_AGENT_ID'))
+# post a message in a thread and create/process a run:
+thread = project.agents.threads.create()
+project.agents.messages.create(thread_id=thread.id, role='user', content=user_query)
+run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
+```
+
+When available, use the Foundry project agent APIs (for example `AIProjectClient` + `project.agents.*`) to run the agent. The backend should:
+
+- create a thread (`project.agents.threads.create()`)
+- post the incoming API request text as the message `content` (`project.agents.messages.create(thread_id=..., role='user', content=request['query'])`)
+- call `project.agents.runs.create_and_process(thread_id=..., agent_id=agent.id)` and parse the returned run/messages for the final answer and citations.
+
+Do not attempt to instantiate or manage Foundry retrieval tool classes in the backend; the agent in Foundry should be pre-configured with any retrieval tools it requires. If the SDK or project-level APIs are missing or misconfigured, raise a clear configuration error. For local development use `STUB_MODE=true`.
        c. After the agent run completes, parse any tool_calls / run_steps to extract citations (URL + snippet) and the final answer. Convert this into the contract response shape: {answer, citations, confidence, fallback}.
   3. Add an optional `FETCH_LINK_CONTENT` env flag for debug/testing that when true allows fetching page content for richer snippets; default is false and the agent should rely on MCP-provided text.
   4. Add unit/integration tests that:
      - Assert STUB_MODE responses are contract-compliant.
      - Mock the Agents SDK or HTTP responses to verify citation extraction and the real-agent path without requiring live keys.
   5. Update documentation and `.env.example` to include PROJECT_ENDPOINT, AI_FOUNDRY_PROJECT (optional), and FETCH_LINK_CONTENT (optional), and explicitly call out not to commit real keys.

- Security & operational notes:
  - Never commit API keys. Update `backend/.env.example` with placeholder variable names.
  - Use timeouts and retries for network calls (e.g., 10–30s timeout and 1–2 retries).
  - Keep the candidate list small (e.g., 2–3) to keep prompts compact and within token limits.

## Next steps (after plan approval)
- Implement the `docs_index` helper and extend `query_service` to call the real agent when STUB_MODE=false.
- Add tests for the real-agent path using a mocked agent response (so CI doesn't require real keys).
- Iterate on prompt text and citation extraction when we test against a real Foundry project.
# research.md — Azure AI Foundry Agent & related SDKs (prototype research)

Date: 2025-08-28

Purpose: capture research findings and open tasks required to lock down SDK/package versions, authentication patterns, and streaming behavior for the grafanacopilot prototype.

---

## Objective

Validate the Python SDKs, streaming patterns, and telemetry/exporter choices so we can pin dependency versions for the grafanacopilot prototype and implement a minimal, stable integration with Azure AI Foundry and MCP retrieval.

### Primary concerns
- Which Python package to use to call the Azure AI Foundry "Responses" API (OpenAI client vs azure-specific SDK).
- Streaming interface for incremental tokens and citation markers.
- Authentication modes (API key vs Microsoft Entra ID / DefaultAzureCredential) and examples.
- Telemetry exporter choices for Application Insights (OpenTelemetry exporter vs opencensus).
- Compatibility and minimal pinned versions for prototype.

---

## Initial findings (web survey)

- `azure-ai-agents` (PyPI) selected for the prototype: **1.1.0** (to be validated/fetched). This package will be used to call the Azure AI Foundry Agent/Responses APIs in the grafanacopilot prototype. We will use API keys (AI_FOUNDRY_API_KEY) for authentication in prototype, simplifying local testing (no azure-identity required for prototype flow).

- `openai` Python library references remain useful as a comparison, but the prototype will rely on `azure-ai-agents` per project decision.

- `azure-monitor-opentelemetry-exporter` (PyPI) appears in preview/beta (`1.0.0b41`); it provides an OpenTelemetry exporter for Application Insights. This is a natural integration point; alternative: `opencensus-ext-azure` (older) or Azure Monitor OpenTelemetry Distro depending on desired stability.

- Azure Foundry docs (Responses API) indicate that the Responses API exposes streaming semantics at the API level. However, the selected SDK `azure-ai-agents==1.1.0` does not expose a streaming interface in this version. For the prototype we will use synchronous (final-response) calls via `azure-ai-agents`. If streaming is required later, we will evaluate alternative SDKs or implement server-side chunking/SSE.

---

## Candidate dependency versions (updated)

- `azure-ai-agents==1.1.0` (primary SDK for Foundry/Responses; prototype default)
- `openai` (not required for prototype, keep as a comparative reference)
- `azure-monitor-opentelemetry-exporter==1.0.0b41` (beta; optional; evaluate stability)
- `asyncpg` (for Postgres): `asyncpg>=0.27.0` (choose latest stable)
- `httpx` (transports): `httpx>=0.24.0` (if needed by SDKs)

> Note: azure-identity is not required for prototype because we will use API keys for Azure AI Foundry access. In production, consider using Managed Identity / DefaultAzureCredential.

---

## Research tasks (parallel) — run these to validate versions and APIs

1. Validate the `azure-ai-agents` PyPI package (1.1.0): confirm package name and APIs for synchronous Responses API calls; capture a minimal synchronous example for final answer + citations and confirm how to pass API key (AI_FOUNDRY_API_KEY) in client initialization or via environment. (Status: OPEN — fetch docs/PyPI page)

2. Confirm that `azure-ai-agents` supports the Responses API; capture a minimal synchronous example that returns final answer and citation metadata; determine canonical fields for citations and confidence.

3. Verify how to pass API key (AI_FOUNDRY_API_KEY) in the `azure-ai-agents` client (e.g., client initialization parameters or environment variable) and confirm whether `base_url` or `project` parameters are required.

4. Confirm telemetry exporter integration and sample code for `azure-monitor-opentelemetry-exporter` using `APPLICATIONINSIGHTS_CONNECTION_STRING` (Status: CHECKED earlier — docs found; verify exact API for Python usage).

5. Validate that `azure-ai-agents==1.1.0` is compatible with Python 3.11 and the other chosen libs.

6. Confirm that streaming-to-frontend is NOT required for the prototype (synchronous responses). Document a migration path to streaming later (SSE vs chunked) and how citation events would be represented when/if streaming is reintroduced.

7. Confirm the MCP approval flow and the pattern for including MCP calls in Responses API; capture sample interaction flow and approval event format (Status: INFO COLLECTED earlier).

8. Finalize pins in `backend/requirements.txt` and implement a quick local smoke test (STUB_MODE default true; switch to real keys in `.env` to test real integration).

---

## Planned findings to record & output

- Final package pins to place in `backend/requirements.txt` and `frontend/package.json`.
- Minimal sample code snippets showing `azure-ai-agents` synchronous usage and `DefaultAzureCredential` usage for future work. (Removed live streaming sample from scope for prototype.)
- Decision & notes on telemetry exporter (prefer `azure-monitor-opentelemetry-exporter` with fallback to `opencensus-ext-azure` for stability).

---

## Actions (next) — reflect decision to use API key auth

- Update `backend/.env` and `frontend/.env` to include AI_FOUNDRY_API_KEY. For prototype, use API key authorization and skip `azure-identity` usage.
- Add research task to verify `azure-ai-agents==1.1.0` API surface and synchronous usage examples (create issue/checklist item to validate with samples).
- If validation is successful, pin `azure-ai-agents==1.1.0` in `backend/requirements.txt` and implement the synchronous sample endpoint using the `azure-ai-agents` client.

---

## Web references (fetched)

- PyPI: `azure-identity` (1.24.0) — https://pypi.org/project/azure-identity/
- PyPI: `openai` (1.102.0) — https://pypi.org/project/openai/
- Azure AI Foundry / Responses API docs — streaming and MCP examples — https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/responses?tabs=python-key
- PyPI: `azure-monitor-opentelemetry-exporter` (1.0.0b41) — https://pypi.org/project/azure-monitor-opentelemetry-exporter/


---

If you'd like, I can:
- pin these candidate versions in `backend/requirements.txt` and create a `requirements.txt` and `package.json` entries for the front-end, then run sample local tests (stub mode) to verify imports at runtime,
- or run more specific fetches (e.g., `openai` changelog or `azure-monitor-opentelemetry-exporter` samples) and append the summarized snippets to this document.

Which of the two would you prefer next? (pin-and-verify vs deeper web fetch summaries)

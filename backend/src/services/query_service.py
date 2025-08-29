"""Query service: prototype implementation with STUB_MODE support and optional Azure agent integration.

When STUB_MODE=true (default), returns canned responses for local testing.
When STUB_MODE=false, attempts to call azure.ai.agents library or the provided
AI_FOUNDRY_ENDPOINT with AI_FOUNDRY_API_KEY. This implementation is best-effort
and will raise clear errors if the configuration is missing.
"""

import os
import asyncio
import logging
import importlib
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def _maybe_await(value):
    if asyncio.iscoroutine(value):
        return await value
    return value


async def run_query(request: Dict[str, Any]) -> Dict[str, Any]:
    """Run a query and return a response conforming to the contract.

    Behavior:
    - If STUB_MODE is enabled (default), return a canned response.
    - Otherwise, try the Azure Agents SDK (if installed). If that fails, try a
      simple HTTP POST to AI_FOUNDRY_ENDPOINT with AI_FOUNDRY_API_KEY.

    The function strives to be robust to different SDK versions and REST
    response shapes by using heuristics to locate the human-readable answer.
    """
    stub = os.environ.get("STUB_MODE", "true").lower() in ("1", "true", "yes")

    if stub:
        # Return a canned response matching the contract
        return {
            "answer": "Stubbed answer: see https://docs.microsoft.com/azure/managed-grafana for details.",
            "citations": [
                {
                    "url": "https://docs.microsoft.com/azure/managed-grafana",
                    "anchor": "getting-started",
                    "snippet": "Use the Azure portal to create a Managed Grafana workspace...",
                }
            ],
            "confidence": 0.92,
            "fallback": False,
            "anchors": ["getting-started"],
        }

    api_key = os.environ.get("AI_FOUNDRY_API_KEY")
    endpoint = os.environ.get("AI_FOUNDRY_ENDPOINT")

    if not api_key or not endpoint:
        raise RuntimeError("AI_FOUNDRY_ENDPOINT and AI_FOUNDRY_API_KEY are required when STUB_MODE is False")

    # FIRST: attempt to use the azure.ai.agents SDK (best-effort)
    try:
        agents_mod = importlib.import_module("azure.ai.agents")
        # Look for a plausible client class
        client_cls = None
        for candidate in ("AgentsClient", "AgentClient", "AgentServiceClient", "AgentRuntimeClient"):
            if hasattr(agents_mod, candidate):
                client_cls = getattr(agents_mod, candidate)
                break

        if client_cls is not None:
            # Try to construct with AzureKeyCredential when available
            try:
                from azure.core.credentials import AzureKeyCredential

                creds = AzureKeyCredential(api_key)
                client = client_cls(endpoint, creds)
            except Exception:
                # Fallback to trying the simpler constructor
                try:
                    client = client_cls(endpoint, api_key)
                except Exception:
                    # Give up on SDK client construction path
                    raise

            prompt_text = request.get("query", "")

            # Find a plausible invocation method on the client
            method = None
            for candidate in (
                "get_response",
                "get_responses",
                "begin_get_responses",
                "run",
                "begin_run",
                "invoke",
                "invoke_agent",
                "create_response",
            ):
                if hasattr(client, candidate):
                    method = getattr(client, candidate)
                    break

            # Some SDKs might expose a `responses` property that is itself callable
            if method is None and hasattr(client, "responses"):
                method = getattr(client, "responses")

            if method is None:
                raise RuntimeError("Found azure.ai.agents client but no known invocation method")

            # Call the method and await if it returns a coroutine
            try:
                out = method(prompt_text) if callable(method) else method
                resp = await _maybe_await(out)
            except Exception as e:
                logger.exception("Error invoking agent SDK method: %s", e)
                raise

            # Extract human-friendly answer text using heuristics
            answer = None
            if isinstance(resp, dict):
                for key in ("output", "answer", "result", "content", "text", "generated_text"):
                    if key in resp:
                        answer = resp[key]
                        break
                if answer is None and "choices" in resp and isinstance(resp["choices"], list) and resp["choices"]:
                    ch = resp["choices"][0]
                    if isinstance(ch, dict):
                        if "message" in ch and isinstance(ch["message"], dict):
                            answer = ch["message"].get("content") or ch["message"].get("text")
                        else:
                            answer = ch.get("text") or str(ch)
            else:
                # Non-dict responses -> stringify
                answer = str(resp)

            if not answer:
                answer = "(no text returned by agent)"

            return {
                "answer": answer,
                "citations": [],
                "confidence": 0.5,
                "fallback": False,
            }
    except Exception as e:
        # SDK path failed; log and continue to REST fallback
        logger.exception("Azure Agents SDK integration not available or failed: %s", e)

    # SECOND: fallback to a simple HTTP call to the configured endpoint
    try:
        headers = {"Content-Type": "application/json"}
        # Try common header names for Azure/OpenAI style services
        headers["api-key"] = api_key
        headers.setdefault("Authorization", f"Bearer {api_key}")

        payload = {"input": request.get("query", "")}

        # Import httpx lazily so STUB_MODE=true environments don't need it installed
        try:
            import httpx
        except Exception:
            raise RuntimeError(
                "httpx is required for non-stub REST requests. Install with: pip install httpx"
            )

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(endpoint, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

            answer = None
            if isinstance(data, dict):
                # openai-style choices
                if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                    choice = data["choices"][0]
                    if isinstance(choice, dict):
                        if "message" in choice and isinstance(choice["message"], dict):
                            answer = choice["message"].get("content") or choice["message"].get("text")
                        else:
                            answer = choice.get("text") or str(choice)
                # Try common top-level fields
                if not answer:
                    for key in ("answer", "output", "result", "content", "generated_text", "text"):
                        if key in data:
                            val = data[key]
                            if isinstance(val, dict):
                                answer = val.get("output") or val.get("text") or str(val)
                            else:
                                answer = val
                            break

            if answer is None:
                # Fallback to raw JSON string
                answer = str(data)

            return {"answer": answer, "citations": [], "confidence": 0.5, "fallback": False}
    except Exception as e:
        logger.exception("Failed to call AI_FOUNDRY_ENDPOINT: %s", e)
        raise RuntimeError("Agent call failed; ensure AI_FOUNDRY_API_KEY and AI_FOUNDRY_ENDPOINT are set, or use STUB_MODE=true") from e

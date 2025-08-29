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

    # New flow: use Foundry project-level APIs (AIProjectClient) with DefaultAzureCredential
    project_endpoint = os.environ.get("PROJECT_ENDPOINT") or os.environ.get("AI_FOUNDRY_ENDPOINT")
    agent_id = os.environ.get("FOUNDARY_AGENT_ID") or os.environ.get("AI_FOUNDRY_AGENT_ID")

    if not project_endpoint:
        raise RuntimeError("PROJECT_ENDPOINT is required when STUB_MODE is False")

    try:
        # Import project-level SDKs
        from azure.ai.projects import AIProjectClient  # type: ignore
        from azure.identity import DefaultAzureCredential  # type: ignore
        from azure.ai.agents.models import ListSortOrder  # type: ignore
    except Exception as e:
        logger.exception("Required Foundry SDKs not available: %s", e)
        raise RuntimeError(
            "Foundry project SDKs are required. Install 'azure-ai-projects'/'azure-ai-agents' or ensure the SDK is available in the environment."
        ) from e

    def _sync_run():
        try:
            project = AIProjectClient(credential=DefaultAzureCredential(), endpoint=project_endpoint)

            # Retrieve the existing agent (agent must be created in Foundry ahead of time)
            if not agent_id:
                # If agent id is not provided, attempt to fail clearly
                raise RuntimeError("FOUNDARY_AGENT_ID (env) must be set when STUB_MODE is False")

            agent = project.agents.get_agent(agent_id)

            # Create or reuse thread and post the user message (content comes from the API request)
            query_text = request.get("query", "")
            provided_thread_id = request.get("thread_id")
            thread_id_to_use = None

            if provided_thread_id:
                # Use the provided thread id (frontend-managed threads)
                thread_id_to_use = provided_thread_id
            else:
                # Create a new thread and keep its id
                thread = project.agents.threads.create()
                thread_id_to_use = getattr(thread, "id", None)

            try:
                if thread_id_to_use:
                    project.agents.messages.create(thread_id=thread_id_to_use, role="user", content=query_text)
            except Exception:
                # best-effort; continue
                pass

            # Create and process a run in the project agent
            run_obj = project.agents.runs.create_and_process(thread_id=thread_id_to_use, agent_id=agent.id)

            # Collect run steps and messages
            run_steps = []
            messages = []
            try:
                run_steps = list(project.agents.run_steps.list(thread_id=thread_id_to_use, run_id=run_obj.id))
            except Exception:
                run_steps = []

            try:
                messages = list(project.agents.messages.list(thread_id=thread_id_to_use, order=ListSortOrder.ASCENDING))
            except Exception:
                try:
                    messages = list(project.agents.messages.list(thread_id=thread_id_to_use))
                except Exception:
                    messages = []

            return run_obj, run_steps, messages, thread_id_to_use
        except Exception as e:
            logger.exception("Project agent run failed: %s", e)
            return None, [], [], None

    try:
        run_obj, run_steps, messages, thread_id = await asyncio.to_thread(_sync_run)
    except Exception as e:
        logger.exception("Agent run thread failed: %s", e)
        run_obj, run_steps, messages, thread_id = None, [], [], None

    # Parse run outputs and messages (similar heuristics as before)
    answer = None
    citations = []

    try:
        for m in messages:
            try:
                text_msgs = getattr(m, "text_messages", None)
                if text_msgs:
                    last_text = text_msgs[-1]
                    text_val = getattr(last_text, "text", None)
                    if text_val is not None:
                        val = getattr(text_val, "value", None) or str(text_val)
                        if isinstance(val, str) and val.strip():
                            answer = val
                if isinstance(m, dict) and not answer:
                    if m.get("role") == "assistant":
                        answer = m.get("text") or m.get("content") or answer
            except Exception:
                pass
    except Exception:
        answer = None

    # Extract tool call outputs for citations
    try:
        for step in run_steps:
            try:
                step_details = None
                if isinstance(step, dict):
                    step_details = step.get("step_details")
                else:
                    step_details = getattr(step, "step_details", None)
                if step_details:
                    tool_calls = []
                    if isinstance(step_details, dict):
                        tool_calls = step_details.get("tool_calls", [])
                    else:
                        tool_calls = getattr(step_details, "tool_calls", [])
                    for call in tool_calls:
                        try:
                            url = (call.get("url") if isinstance(call, dict) else getattr(call, "url", None)) or (call.get("target") if isinstance(call, dict) else getattr(call, "target", None))
                            snippet = (call.get("result") if isinstance(call, dict) else getattr(call, "result", None)) or (call.get("content") if isinstance(call, dict) else getattr(call, "content", None))
                            if url:
                                citations.append({"url": url, "snippet": snippet})
                        except Exception:
                            continue
            except Exception:
                continue
    except Exception:
        citations = []

    if not answer:
        try:
            if isinstance(run_obj, dict):
                for key in ("output", "result", "answer", "content"):
                    if key in run_obj:
                        answer = run_obj.get(key)
                        break
        except Exception:
            pass

    if not answer:
        raise RuntimeError("Agent run did not produce an answer")

    return {"answer": answer, "citations": citations, "confidence": 0.9, "fallback": False, "thread_id": thread_id}


async def create_thread(pseudo_user_id: str | None = None) -> Dict[str, Any]:
    """Create a Foundry thread and return its id.

    In STUB_MODE this returns a generated UUID. Otherwise it calls the
    project-level API to create a thread and returns {"thread_id": id}.
    """
    stub = os.environ.get("STUB_MODE", "true").lower() in ("1", "true", "yes")
    if stub:
        import uuid

        return {"thread_id": str(uuid.uuid4())}

    project_endpoint = os.environ.get("PROJECT_ENDPOINT") or os.environ.get("AI_FOUNDRY_ENDPOINT")
    if not project_endpoint:
        raise RuntimeError("PROJECT_ENDPOINT is required when STUB_MODE is False")

    try:
        from azure.ai.projects import AIProjectClient  # type: ignore
        from azure.identity import DefaultAzureCredential  # type: ignore
    except Exception as e:
        logger.exception("Foundry SDK not available: %s", e)
        raise RuntimeError("Foundry project SDK not available; install azure-ai-projects or ensure the SDK is on PYTHONPATH") from e

    try:
        project = AIProjectClient(credential=DefaultAzureCredential(), endpoint=project_endpoint)
        thread = project.agents.threads.create()
        return {"thread_id": getattr(thread, "id", None)}
    except Exception as e:
        logger.exception("Failed to create Foundry thread: %s", e)
        raise RuntimeError("Failed to create Foundry thread") from e

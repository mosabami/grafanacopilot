"""API endpoints for the Grafana Copilot prototype.

Endpoints implemented (minimal, prototype-ready):
- POST /api/admin/sources
- POST /api/query
- POST /api/telemetry
- GET /api/health

These handlers rely on the services in `backend/src/services` and fall back to
in-memory behavior if DB or services are unavailable.
"""

from fastapi import APIRouter, Header, HTTPException, status, Request
from pydantic import BaseModel
from typing import Any, List, Optional
import os

router = APIRouter()


# Request / response models
class AdminSourceRequest(BaseModel):
    url: str
    title: Optional[str] = None
    priority: Optional[int] = 100


class Citation(BaseModel):
    url: str
    anchor: Optional[str] = None
    snippet: Optional[str] = None


class QueryRequest(BaseModel):
    query: str
    pseudo_user_id: Optional[str] = None
    page_context: Optional[dict] = None


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float
    fallback: bool
    anchors: Optional[List[str]] = None


@router.post("/api/admin/sources")
async def post_admin_sources(payload: AdminSourceRequest, x_api_key: Optional[str] = Header(None)) -> Any:
    admin_key = os.environ.get("ADMIN_API_KEY")
    if admin_key and x_api_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    # Prefer using the sources_service if available
    try:
        from backend.src.services.sources_service import add_source
        created = await add_source(payload)
        return created
    except Exception:
        # Fallback: return an echo with generated id
        import uuid

        return {"id": str(uuid.uuid4()), "url": payload.url, "title": payload.title, "priority": payload.priority}


@router.post("/api/query", response_model=QueryResponse)
async def post_query(payload: QueryRequest) -> QueryResponse:
    # Run query via service (stubbed if STUB_MODE=true)
    try:
        from backend.src.services.query_service import run_query
        try:
            payload_data = payload.model_dump()
        except Exception:
            # Fallback for Pydantic v1 compatibility
            payload_data = payload.dict()
        res = await run_query(payload_data)
        # Minimal validation happens via response_model
        return QueryResponse(**res)
    except Exception as e:
        # If something is misconfigured, expose a clear error in prototype
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/telemetry")
async def post_telemetry(payload: dict) -> dict:
    # Try to record telemetry via telemetry_service, fall back to console log
    try:
        from backend.src.services.telemetry_service import record_event
        await record_event(payload)
        return {"status": "accepted"}
    except Exception:
        import logging

        logging.info("Telemetry event (console): %s", payload)
        return {"status": "accepted"}


@router.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}


# @router.get("/api/health/db")
# async def health_db(request: Request) -> dict:
#     """Return DB initialization status set during startup.

#     Example return:
#       {"db_init": {"sources": "created", "usage_events": "already_existed"}}
#     """
#     status_info = getattr(request.app.state, "db_init_status", None)
#     if status_info is None:
#         return {"db": "unknown", "tables": None}
#     return {"db_init": status_info}

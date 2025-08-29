"""FastAPI app entrypoint for Grafana Copilot prototype."""

import os
import sys
# Make the repository root (two levels up from this file) available on sys.path so
# fully-qualified imports such as `backend.src.api` work even when running the
# script from the `backend` directory (python src/app.py).
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# Attempt to load a local .env (backend/.env) for local development. This makes
# running `python src/app.py` pick up STUB_MODE, AI_FOUNDRY_API_KEY, etc. without
# needing to export them in the shell. Fail silently if python-dotenv is not
# installed (it's optional for production containers where env vars are injected).
try:
    from dotenv import load_dotenv

    dotenv_path = os.path.join(REPO_ROOT, "backend", ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        # Fall back to default behavior of load_dotenv() which searches parent dirs
        load_dotenv()
except Exception:
    # python-dotenv not available or loading failed; ignore and continue
    pass

from fastapi import FastAPI

# Initialize structured logging as early as possible (best-effort)
try:
    from backend.src.observability import configure_logging

    configure_logging()
except Exception:
    # Observability is optional in the prototype; ignore failures here
    pass


def create_app() -> FastAPI:
    app = FastAPI(title="Grafana Copilot Prototype")

    # Attempt to enable Application Insights / OpenTelemetry exporter if configured
    try:
        from backend.src.observability import enable_appinsights_if_configured

        try:
            ok = enable_appinsights_if_configured()
            if ok:
                import logging

                logging.getLogger(__name__).info("Application Insights exporter configured")
        except Exception:
            # ignore failures during optional instrumentation
            pass
    except Exception:
        pass

    @app.get("/api/health")
    async def health():
        return {"status": "ok"}

    # # Try to initialise DB on startup so `/api/health/db` can report table status.
    # @app.on_event("startup")
    # async def _ensure_db():
    #     import logging
    #     try:
    #         # Import lazily so missing DB deps don't block the whole app
    #         from db import create_all

    #         status = await create_all()
    #         # Persist status on app.state so the health endpoint can report
    #         app.state.db_init_status = status
    #         logging.info("DB initialization status: %s", status)
    #     except Exception as e:
    #         logging.exception("DB initialization failed (non-fatal): %s", e)

    # Import API router lazily to avoid import-time errors if services are not created yet
    api_router = None
    import logging
    try:
        # Preferred: absolute package import (works when REPO_ROOT is placed on sys.path)
        from backend.src.api import router as api_router  # type: ignore
    except Exception:
        try:
            # fallback: module-style import if running as a package from repo root
            from src.api import router as api_router  # type: ignore
        except Exception:
            try:
                # fallback: plain import when running the script from backend/src (python src/app.py)
                from api import router as api_router  # type: ignore
            except Exception:
                logging.exception("Failed to import API router; API routes will not be available")
                api_router = None

    if api_router is not None:
        app.include_router(api_router)

    return app


app = create_app()

if __name__ == "__main__":
    # Programmatic entrypoint: `python backend/src/app.py`
    import os
    try:
        import uvicorn
    except Exception as e:
        print("uvicorn is not installed. Install with: pip install 'uvicorn[standard]'")
        raise

    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", "8000"))
    reload_flag = os.environ.get("APP_RELOAD", "false").lower() in ("1", "true", "yes")

    if reload_flag:
        # When reload is requested, run via an import path (so reload can re-import modules).
        # Try the package-style import first, then fallback to the relative import.
        import importlib

        import_path = None
        try:
            importlib.import_module("backend.src.app")
            import_path = "backend.src.app:app"
        except Exception:
            try:
                importlib.import_module("src.app")
                import_path = "src.app:app"
            except Exception:
                # last-resort: use the backend import path
                import_path = "backend.src.app:app"

        uvicorn.run(import_path, host=host, port=port, reload=True)
    else:
        # Run the already-created app object directly. This makes
        # `python src/app.py` start the server regardless of the working directory.
        uvicorn.run(app, host=host, port=port, reload=False)

"""Minimal observability helpers for prototype.

- Configure Python logging (JSON-friendly formatting)
- Optional: wire AppInsights exporter when `APPINSIGHTS_CONNECTION_STRING` is present
"""

import logging
import os


def configure_logging():
    level = os.environ.get("LOG_LEVEL", "INFO")
    logging.basicConfig(level=level)
    logging.getLogger("uvicorn.access").setLevel(level)


def enable_appinsights_if_configured():
    conn_str = os.environ.get("APPINSIGHTS_CONNECTION_STRING")
    if not conn_str:
        return False
    # Try to configure OpenTelemetry exporter if installed; be optional.
    try:
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.azuremonitor import AzureMonitorTraceExporter

        resource = Resource.create({"service.name": "grafanacopilot-backend"})
        provider = TracerProvider(resource=resource)
        exporter = AzureMonitorTraceExporter(connection_string=conn_str)
        span_processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(span_processor)
        return True
    except Exception:
        # No telemetry exports available; silently skip for prototype
        return False

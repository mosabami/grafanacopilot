import os
import sys
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import pytest
from backend.src.models.sources import Source
from backend.src.models.usage_events import UsageEvent


def test_source_model_basic():
    s = Source(url="https://example.com", title="example")
    assert s.url.startswith("https://")


def test_usage_event_model_basic():
    ue = UsageEvent(event_type="query")
    assert ue.event_type == "query"

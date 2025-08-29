import os
from fastapi.testclient import TestClient


def test_stub_query_response_shape():
    """Integration-style unit test: POST /api/query returns the stubbed shape.

    This test uses FastAPI's TestClient to exercise the in-memory app without
    running a network server. STUB_MODE is set to true to ensure the canned
    response path is taken.
    """
    # Ensure stub-mode for the scope of this test
    os.environ.setdefault("STUB_MODE", "true")

    # Import the app lazily so env var takes effect
    from backend.src.app import app

    client = TestClient(app)

    payload = {"query": "How do I get started with Azure Managed Grafana?"}
    r = client.post("/api/query", json=payload)

    assert r.status_code == 200, f"Unexpected status: {r.status_code}, body: {r.text}"

    data = r.json()

    # Basic shape
    assert "answer" in data and isinstance(data["answer"], str)
    assert "citations" in data and isinstance(data["citations"], list)
    assert "confidence" in data and (isinstance(data["confidence"], float) or isinstance(data["confidence"], int))
    assert "fallback" in data and isinstance(data["fallback"], bool)

    # If citations are present, ensure they have at least a url field
    for c in data["citations"]:
        assert isinstance(c, dict)
        assert "url" in c and isinstance(c["url"], str)

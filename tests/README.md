Unit tests are colocated with backend code in `backend/tests/unit`.
Integration tests remain under `tests/integration`.

To run all tests from the repository root (recommended):

    pytest -q

Run just unit tests:

    pytest backend/tests/unit

Run just integration tests:

    pytest tests/integration

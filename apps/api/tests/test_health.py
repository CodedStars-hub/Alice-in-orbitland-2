import pytest
from fastapi.testclient import TestClient
from lunar_api.app import create_app


def test_health() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "scientific_features": "not_implemented"}


def test_cors_allowlist(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LUNAR_CORS_ORIGINS", "http://localhost:5173")
    with TestClient(create_app()) as client:
        allowed = client.get("/api/v1/health", headers={"Origin": "http://localhost:5173"})
        denied = client.get("/api/v1/health", headers={"Origin": "https://untrusted.example"})
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
    assert "access-control-allow-origin" not in denied.headers
    assert "access-control-allow-credentials" not in allowed.headers


def test_reject_wildcard(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LUNAR_CORS_ORIGINS", "*")
    with pytest.raises(ValueError, match="explicit HTTP"):
        create_app()

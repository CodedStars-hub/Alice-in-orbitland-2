import lunar_core
from fastapi.testclient import TestClient
from lunar_api.app import create_app


def test_api_and_core_install_together() -> None:
    assert lunar_core.__version__ == "0.1.0"
    with TestClient(create_app()) as client:
        assert client.get("/api/v1/health").json()["scientific_features"] == "not_implemented"

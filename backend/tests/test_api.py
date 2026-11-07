from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_is_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_market_catalog_has_all_market_groups():
    response = client.get("/api/v1/markets")
    assert response.status_code == 200
    groups = {item["group"] for item in response.json()}
    assert {"forex", "crypto", "volatility", "deriv_synthetic"} <= groups


def test_market_catalog_can_filter_by_group():
    response = client.get("/api/v1/markets?group=forex")
    assert response.status_code == 200
    assert all(item["group"] == "forex" for item in response.json())


def test_signal_preview_abstains_without_verified_data():
    response = client.get("/api/v1/signals/preview/EURUSD")
    assert response.status_code == 200
    assert response.json()["direction"] == "NO_TRADE"
    assert response.json()["confidence"] == 0

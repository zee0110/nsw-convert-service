"""API-level tests for the conversion service."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_convert_length():
    resp = client.post("/convert/length", json={"value": 1, "from_unit": "km", "to_unit": "m"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 1000.0


def test_convert_currency():
    resp = client.post(
        "/convert/currency", json={"value": 100, "from_unit": "AUD", "to_unit": "USD"}
    )
    assert resp.status_code == 200
    assert resp.json()["result"] == 66.0


def test_unknown_kind_404():
    resp = client.post("/convert/volume", json={"value": 1, "from_unit": "l", "to_unit": "ml"})
    assert resp.status_code == 404


def test_unknown_unit_400():
    resp = client.post("/convert/length", json={"value": 1, "from_unit": "parsec", "to_unit": "m"})
    assert resp.status_code == 400


def test_validation_error_422():
    resp = client.post("/convert/length", json={"from_unit": "km", "to_unit": "m"})
    assert resp.status_code == 422

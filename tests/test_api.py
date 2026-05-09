from __future__ import annotations

from fastapi.testclient import TestClient

from sgs_calculator.example import EXAMPLE_BATTLE
from sgs_calculator.main import app


client = TestClient(app)


def test_example_endpoint_returns_battle_json() -> None:
    response = client.get("/api/example")

    assert response.status_code == 200
    assert response.json()["meta"]["seed"] == 1941


def test_validate_endpoint_accepts_example() -> None:
    response = client.post("/api/validate", json=EXAMPLE_BATTLE)

    assert response.status_code == 200
    assert response.json() == {"valid": True, "errors": []}


def test_validate_endpoint_reports_schema_errors() -> None:
    bad = {"attacker": {"name": "A", "units": []}}

    response = client.post("/api/validate", json=bad)

    assert response.status_code == 200
    assert response.json()["valid"] is False
    assert response.json()["errors"]


def test_simulate_endpoint_returns_report() -> None:
    response = client.post("/api/simulate", json=EXAMPLE_BATTLE)

    assert response.status_code == 200
    body = response.json()
    assert body["final"]["winner"] == "Commonwealth"
    assert body["rounds"][0]["label"] == "Setup"


def test_simulate_endpoint_rejects_malformed_json() -> None:
    response = client.post(
        "/api/simulate",
        content="{",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422

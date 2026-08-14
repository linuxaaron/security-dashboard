from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_summary():
    with TestClient(app) as client:
        response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert "security_score" in data
    assert "risk_level" in data
    assert "assets" in data
    assert "vulnerabilities" in data
    assert "critical_vulnerabilities" in data
    assert "high_vulnerabilities" in data
    assert "security_events" in data
    assert "risk_components" in data

    assert 0 <= data["security_score"] <= 100
    assert data["risk_level"] in {
        "low",
        "medium",
        "high",
        "critical",
    }


def test_dashboard_risk_components():
    with TestClient(app) as client:
        response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200

    components = response.json()["risk_components"]

    assert set(components) == {
        "cvss",
        "vulnerabilities",
        "assets",
        "events",
    }

    for value in components.values():
        assert 0 <= value <= 100

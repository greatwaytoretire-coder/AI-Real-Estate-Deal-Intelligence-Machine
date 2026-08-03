from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_optimize_portfolio():

    response = client.post(
        "/api/v1/portfolio-optimization",
        json={
            "portfolio_id": "PORT-API-001",
            "total_value": 500000,
            "equity": 200000,
            "annual_income": 60000,
            "annual_expenses": 20000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == "PORT-API-001"
    assert "health_score" in data


def test_invalid_portfolio():

    response = client.post(
        "/api/v1/portfolio-optimization",
        json={
            "portfolio_id": "BAD",
            "total_value": 0,
            "equity": 0,
            "annual_income": 1000,
            "annual_expenses": 500,
        },
    )

    assert response.status_code >= 400
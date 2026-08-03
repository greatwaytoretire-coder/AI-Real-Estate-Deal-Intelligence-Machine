from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_create_portfolio_api():

    response = client.post(
        "/api/v1/portfolio",
        json={
            "portfolio_id": "PORT-API-001",
            "owner_id": "OWNER-API-001",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == "PORT-API-001"



def test_portfolio_performance_api():

    response = client.get(
        "/api/v1/portfolio/PORT-API-001/performance"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == "PORT-API-001"
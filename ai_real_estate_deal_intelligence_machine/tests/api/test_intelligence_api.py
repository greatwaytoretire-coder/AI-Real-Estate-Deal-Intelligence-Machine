from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.api.app import app


client = TestClient(app)


def test_intelligence_analysis_endpoint():

    response = client.post(
        "/api/v1/intelligence/analyze",
        json={
            "property_id": "PROP-001",
            "purchase_price": 150000,
            "estimated_value": 250000,
            "repair_cost": 35000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["property_id"] == "PROP-001"

    assert data["projected_profit"] == 65000

    assert data["investment_grade"] == "STRONG"

    assert data["recommended_action"] == "PURSUE"


def test_intelligence_analysis_validation():

    response = client.post(
        "/api/v1/intelligence/analyze",
        json={
            "property_id": "PROP-001",
            "purchase_price": "invalid",
        },
    )

    assert response.status_code == 422
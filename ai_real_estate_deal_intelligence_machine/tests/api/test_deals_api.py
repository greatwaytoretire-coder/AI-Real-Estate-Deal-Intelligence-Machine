from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.api.app import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "operational"



def test_analyze_deal_endpoint():

    response = client.post(
        "/api/v1/deals/analyze",
        json={
            "property_id": "PROP-001",
            "address": "123 Main Street",
            "purchase_price": 150000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["property_id"] == "PROP-001"

    assert data["analysis_status"] == "completed"
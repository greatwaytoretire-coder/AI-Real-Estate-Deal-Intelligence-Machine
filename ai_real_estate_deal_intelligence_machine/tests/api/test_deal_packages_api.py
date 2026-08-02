from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_deal_package_endpoint():

    response = client.post(
        "/api/v1/deal-packages/build",
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

    assert data["status"] == "COMPLETED"

    assert data["deal_score"] > 0

    assert data["projected_profit"] > 0
from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app

client = TestClient(app)


def test_generate_seller_outreach():

    response = client.post(
        "/api/v1/seller-outreach/generate",
        json={
            "seller_id": "SELLER-001",
            "property_id": "PROP-001",
            "motivation_level": "high",
            "preferred_channel": "phone",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["seller_id"] == "SELLER-001"
    assert data["property_id"] == "PROP-001"
    assert data["outreach_channel"] == "phone"
    assert data["priority"] == "HIGH"
    assert data["status"] == "READY"
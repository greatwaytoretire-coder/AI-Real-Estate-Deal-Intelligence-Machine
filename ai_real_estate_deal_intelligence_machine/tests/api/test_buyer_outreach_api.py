from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_generate_buyer_outreach_api():

    response = client.post(
        "/api/v1/buyer-outreach/generate",
        json={
            "property_id": "PROP-001",
            "buyer_id": "BUYER-001",
            "buyer_type": "cash_investor",
            "preferred_channel": "email",
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert data["property_id"] == "PROP-001"

    assert data["buyer_id"] == "BUYER-001"

    assert data["outreach_channel"] == "email"

    assert data["priority"] == "HIGH"

    assert data["status"] == "READY"

    assert "PROP-001" in data["message"]
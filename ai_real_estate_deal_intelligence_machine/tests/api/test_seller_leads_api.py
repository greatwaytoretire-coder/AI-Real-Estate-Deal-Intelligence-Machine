from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_create_seller_lead_analysis():

    response = client.post(
        "/api/v1/seller-leads/analyze",
        json={
            "market": "Test Market",
            "property_address": "789 Pine Street",
            "estimated_value": 350000,
            "motivation_score": 90,
            "distress_signals": [
                "Vacant Property",
                "Foreclosure Risk",
            ],
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    assert "seller_id" in data[0]

    assert "priority_score" in data[0]

    assert "recommendation" in data[0]
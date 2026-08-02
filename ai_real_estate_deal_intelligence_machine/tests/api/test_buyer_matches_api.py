from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_buyer_matches_endpoint():

    response = client.post(
        "/api/v1/buyer-matches",
        json={
            "property_id": "PROP-001",
            "purchase_price": 150000,
            "estimated_value": 250000,
            "repair_cost": 35000,
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert isinstance(data, list)


    assert len(data) > 0


    buyer = data[0]


    assert "buyer_id" in buyer

    assert "buyer_name" in buyer

    assert "match_score" in buyer

    assert "reasoning" in buyer
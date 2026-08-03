from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_analyze_negotiation_api():

    response = client.post(
        "/api/v1/negotiations/analyze",
        json={
            "deal_id": "DEAL-001",
            "current_offer": 200000,
            "seller_counter_offer": 200000,
            "arv": 350000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["deal_id"] == "DEAL-001"

    assert "recommended_offer" in data

    assert "acceptance_probability" in data



def test_negotiation_counter_offer_api():

    response = client.post(
        "/api/v1/negotiations/analyze",
        json={
            "deal_id": "DEAL-002",
            "current_offer": 200000,
            "seller_counter_offer": 230000,
            "arv": 350000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["negotiation_stage"] in [
        "Negotiating",
        "Counter Offer Received",
        "Accepted",
    ]

    assert data["recommended_offer"] > 0
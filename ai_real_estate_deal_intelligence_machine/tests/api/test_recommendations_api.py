from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.api.app import app


client = TestClient(app)


def test_generate_recommendation_endpoint():

    response = client.post(
        "/api/v1/recommendations/generate",
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

    assert data["recommendation"] in [
        "ACQUIRE",
        "PURSUE",
    ]

    assert data["priority"] in [
        "HIGH",
        "MEDIUM",
    ]

    assert len(
        data["reasoning"]
    ) > 0


def test_generate_recommendation_low_score():

    response = client.post(
        "/api/v1/recommendations/generate",
        json={
            "property_id": "PROP-002",
            "purchase_price": 220000,
            "estimated_value": 230000,
            "repair_cost": 20000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["property_id"] == "PROP-002"

    assert data["recommendation"] in [
        "NEGOTIATE",
        "PASS",
    ]
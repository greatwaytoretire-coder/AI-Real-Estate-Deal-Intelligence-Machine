from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_generate_acquisition_offer_api():

    response = client.post(
        "/api/v1/acquisition-offers/generate",
        json={
            "property_id": "PROPERTY-001",
            "arv": 300000,
            "repair_cost": 50000,
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert data["property_id"] == "PROPERTY-001"

    assert data["arv"] == 300000

    assert data["repair_cost"] == 50000

    assert data["recommended_offer"] == 190000

    assert data["confidence_score"] > 0

    assert len(data["reasoning"]) > 0



def test_generate_offer_with_custom_margin():

    response = client.post(
        "/api/v1/acquisition-offers/generate",
        json={
            "property_id": "PROPERTY-002",
            "arv": 500000,
            "repair_cost": 100000,
            "desired_profit_margin": 0.25,
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert data["recommended_offer"] == 275000
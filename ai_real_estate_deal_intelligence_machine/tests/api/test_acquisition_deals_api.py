from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_get_acquisition_deals():

    response = client.get(
        "/api/v1/acquisition-deals"
    )


    assert response.status_code == 200


    data = response.json()


    assert len(data) >= 1


    assert data[0]["deal_id"] == "DEAL-001"



def test_advance_acquisition_deal():

    response = client.post(
        "/api/v1/acquisition-deals/advance",
        json={
            "deal_id": "DEAL-001",
            "new_status": "Offer Ready",
            "note": "Offer package prepared.",
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert data["deal_id"] == "DEAL-001"

    assert data["status"] == "Offer Ready"

    assert (
        "Offer package prepared."
        in data["notes"]
    )
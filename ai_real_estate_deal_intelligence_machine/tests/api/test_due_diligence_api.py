from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_create_due_diligence_api():

    response = client.post(
        "/api/v1/due-diligence",
        json={
            "review_id": "DD-API-001",
            "property_address": "500 River Road",
            "contract_id": "CONTRACT-API-001",
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert data["review_id"] == "DD-API-001"
    assert data["property_address"] == "500 River Road"



def test_get_due_diligence_api():

    response = client.get(
        "/api/v1/due-diligence"
    )


    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )
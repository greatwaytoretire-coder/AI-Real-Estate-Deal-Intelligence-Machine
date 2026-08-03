from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_create_closing_api():

    response = client.post(
        "/api/v1/closings",
        json={
            "closing_id": "CLOSING-API-001",
            "contract_id": "CONTRACT-API-001",
            "property_address": "500 River Road",
            "title_company": "ABC Title",
            "closing_date": "2026-09-01",
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert data["closing_id"] == "CLOSING-API-001"
    assert data["contract_id"] == "CONTRACT-API-001"
    assert data["status"] == "Scheduled"



def test_get_closings_api():

    response = client.get(
        "/api/v1/closings"
    )


    assert response.status_code == 200


    data = response.json()


    assert isinstance(
        data,
        list,
    )
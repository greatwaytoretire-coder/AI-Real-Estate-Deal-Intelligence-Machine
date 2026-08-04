from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_create_financial_record():

    response = client.post(
        "/api/v1/property-financials",
        json={
            "record_id": "FIN-001",
            "property_id": "PROP-001",
            "income": 5000,
            "expenses": 2000,
            "period": "2026-08",
        },
    )


    assert response.status_code == 200



def test_invalid_income():

    response = client.post(
        "/api/v1/property-financials",
        json={
            "record_id": "FIN-002",
            "property_id": "PROP-002",
            "income": -100,
            "expenses": 500,
            "period": "2026-08",
        },
    )


    assert response.status_code == 400
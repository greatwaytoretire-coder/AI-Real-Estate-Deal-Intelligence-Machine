from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_create_rent_payment():

    response = client.post(
        "/api/v1/rent-collection",
        json={
            "payment_id": "PAY-001",
            "tenant_id": "TENANT-001",
            "property_id": "PROP-001",
            "amount": 1500,
            "payment_date": "2026-08-01",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["payment_id"] == "PAY-001"



def test_invalid_amount():

    response = client.post(
        "/api/v1/rent-collection",
        json={
            "payment_id": "PAY-002",
            "tenant_id": "TENANT-002",
            "property_id": "PROP-002",
            "amount": 0,
            "payment_date": "2026-08-01",
        },
    )

    assert response.status_code == 400
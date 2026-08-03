from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_create_contract_api():

    response = client.post(
        "/api/v1/contracts",
        json={
            "contract_id": "CONTRACT-API-001",
            "seller_id": "SELLER-API-001",
            "property_address": "100 Market Street",
            "purchase_price": 300000,
            "earnest_money": 15000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["contract_id"] == "CONTRACT-API-001"
    assert data["seller_id"] == "SELLER-API-001"
    assert data["purchase_price"] == 300000



def test_get_contracts_api():

    response = client.get(
        "/api/v1/contracts"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
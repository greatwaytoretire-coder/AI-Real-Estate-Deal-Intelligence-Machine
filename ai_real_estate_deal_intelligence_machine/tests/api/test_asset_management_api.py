from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_create_asset_api():

    response = client.post(
        "/api/v1/asset-management",
        json={
            "asset_id": "ASSET-API-001",
            "property_address": "500 River Road",
            "acquisition_price": 350000,
            "closing_date": "2026-08-03",
            "strategy": "Rental",
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert data["asset_id"] == "ASSET-API-001"



def test_get_asset_performance_api():

    response = client.get(
        "/api/v1/asset-management/ASSET-API-001/performance"
    )


    assert response.status_code == 200

    data = response.json()

    assert data["asset_id"] == "ASSET-API-001"
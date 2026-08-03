from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_create_tenant_api():

    response = client.post(
        "/api/v1/tenant-management",
        json={
            "tenant_id": "TENANT-001",
            "property_id": "PROPERTY-001",
            "tenant_name": "John Smith",
            "monthly_rent": 1500,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tenant_id"] == "TENANT-001"


def test_get_tenants_api():

    response = client.get(
        "/api/v1/tenant-management"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )
from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app

client = TestClient(app)


def test_create_lease_api():

    response = client.post(
        "/api/v1/lease-management",
        json={
            "lease_id": "LEASE-001",
            "tenant_id": "TENANT-001",
            "property_id": "PROPERTY-001",
            "start_date": "2026-01-01",
            "end_date": "2027-01-01",
            "monthly_rent": 1500,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["lease_id"] == "LEASE-001"
    assert data["status"] == "ACTIVE"


def test_invalid_rent():

    response = client.post(
        "/api/v1/lease-management",
        json={
            "lease_id": "LEASE-002",
            "tenant_id": "TENANT-002",
            "property_id": "PROPERTY-002",
            "start_date": "2026-01-01",
            "end_date": "2027-01-01",
            "monthly_rent": 0,
        },
    )

    assert response.status_code == 400
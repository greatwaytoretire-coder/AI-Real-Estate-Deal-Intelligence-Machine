from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)


def test_create_inspection():

    response = client.post(
        "/api/v1/inspection-management",
        json={
            "inspection_id": "INS-001",
            "property_id": "PROP-001",
            "inspector_name": "John Inspector",
            "inspection_date": "2026-09-01",
            "condition": "GOOD",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["inspection_id"] == "INS-001"
    assert data["property_id"] == "PROP-001"
    assert data["inspector_name"] == "John Inspector"
    assert data["condition"] == "GOOD"


def test_get_inspections():

    response = client.get(
        "/api/v1/inspection-management"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list,
    )
from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_create_maintenance():

    response = client.post(
        "/api/v1/maintenance",
        json={
            "work_order_id": "WO-100",
            "property_id": "PROP-100",
            "description": "Fix electrical issue",
            "priority": "HIGH",
            "estimated_cost": 750,
        },
    )

    assert response.status_code == 200

    assert response.json()["work_order_id"] == "WO-100"



def test_invalid_priority():

    response = client.post(
        "/api/v1/maintenance",
        json={
            "work_order_id": "WO-101",
            "property_id": "PROP-101",
            "description": "Repair",
            "priority": "INVALID",
            "estimated_cost": 100,
        },
    )

    assert response.status_code != 500
from fastapi.testclient import TestClient

from ai_real_estate_deal_intelligence_machine.main import app


client = TestClient(app)



def test_get_acquisition_workflows():

    response = client.get(
        "/api/v1/acquisition-workflows"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        list,
    )

    assert len(data) > 0

    assert (
        data[0]["seller_id"]
        ==
        "SELLER-001"
    )



def test_advance_acquisition_workflow():

    response = client.post(
        "/api/v1/acquisition-workflows/advance",
        json={
            "seller_id": "SELLER-001",
            "new_stage": "Contact Attempted",
            "note": "Seller contacted successfully.",
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        data["seller_id"]
        ==
        "SELLER-001"
    )


    assert (
        data["current_stage"]
        ==
        "Contact Attempted"
    )


    assert (
        "Seller contacted successfully."
        in
        data["notes"]
    )
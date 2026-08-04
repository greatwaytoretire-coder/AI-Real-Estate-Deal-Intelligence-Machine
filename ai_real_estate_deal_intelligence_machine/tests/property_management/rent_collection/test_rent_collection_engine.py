from ai_real_estate_deal_intelligence_machine.rent_collection.rent_collection_engine import (
    RentCollectionEngine,
)


def test_create_rent_payment():

    engine = RentCollectionEngine()

    payment = engine.create_rent_payment(
        payment_id="PAY-001",
        tenant_id="TENANT-001",
        property_id="PROP-001",
        amount=1500,
        payment_date="2026-08-01",
    )

    assert payment["payment_id"] == "PAY-001"
    assert payment["tenant_id"] == "TENANT-001"
    assert payment["amount"] == 1500



def test_get_rent_payments():

    engine = RentCollectionEngine()

    engine.create_rent_payment(
        payment_id="PAY-002",
        tenant_id="TENANT-002",
        property_id="PROP-002",
        amount=1800,
        payment_date="2026-08-01",
    )

    payments = engine.get_rent_payments()

    assert len(payments) == 1
    assert payments[0]["payment_id"] == "PAY-002"
from ai_real_estate_deal_intelligence_machine.property_financials.property_financials_engine import (
    PropertyFinancialsEngine,
)


def test_create_financial_record():

    engine = PropertyFinancialsEngine()

    record = engine.create_financial_record(
        record_id="FIN-001",
        property_id="PROP-001",
        income=3000,
        expenses=1000,
        period="2026-08",
    )


    assert record["record_id"] == "FIN-001"
    assert record["noi"] == 2000



def test_get_financial_records():

    engine = PropertyFinancialsEngine()

    engine.create_financial_record(
        record_id="FIN-002",
        property_id="PROP-002",
        income=4000,
        expenses=1500,
        period="2026-08",
    )


    records = engine.get_financial_records()


    assert len(records) == 1
    assert records[0]["property_id"] == "PROP-002"
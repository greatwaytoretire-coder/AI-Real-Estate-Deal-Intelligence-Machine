from ai_real_estate_deal_intelligence_machine.providers.county_records.county_records_provider import (
    CountyRecordsProvider,
)


def test_county_records_provider_config():

    provider = CountyRecordsProvider()

    config = provider.get_config()

    assert config.name == "county_records_provider"


def test_county_records_fetch():

    provider = CountyRecordsProvider()

    records = provider.fetch(
        {
            "county": "Maricopa",
            "state": "AZ",
        }
    )

    assert len(records) == 1
    assert records[0]["parcel_id"] == "PARCEL-001"


def test_county_records_fields():

    provider = CountyRecordsProvider()

    record = provider.fetch({})[0]

    assert "owner_name" in record
    assert "assessed_value" in record
    assert "tax_status" in record
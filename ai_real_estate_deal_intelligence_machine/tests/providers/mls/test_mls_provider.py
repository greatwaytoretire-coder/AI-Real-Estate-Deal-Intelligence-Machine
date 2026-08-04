from ai_real_estate_deal_intelligence_machine.providers.mls.mls_provider import (
    MLSProvider,
)


def test_mls_provider_config():

    provider = MLSProvider()

    config = provider.get_config()

    assert config.name == "mls_provider"



def test_mls_provider_fetch():

    provider = MLSProvider()

    results = provider.fetch(
        {
            "city": "Phoenix",
            "state": "AZ",
        }
    )

    assert len(results) == 1

    listing = results[0]

    assert listing["listing_id"] == "MLS-001"

    assert listing["status"] == "Active"



def test_mls_listing_fields():

    provider = MLSProvider()

    listing = provider.fetch({})[0]

    assert "price" in listing

    assert "bedrooms" in listing

    assert "square_feet" in listing

    assert listing["listing_source"] == "Mock MLS"
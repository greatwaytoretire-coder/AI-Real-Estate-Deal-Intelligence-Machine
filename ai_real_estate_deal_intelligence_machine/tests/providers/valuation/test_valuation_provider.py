from ai_real_estate_deal_intelligence_machine.providers.valuation.valuation_provider import (
    ValuationProvider,
)


def test_valuation_provider_config():

    provider = ValuationProvider()

    config = provider.get_config()

    assert config.name == "valuation_provider"


def test_valuation_provider_fetch():

    provider = ValuationProvider()

    results = provider.fetch(
        {
            "address": "500 Intelligence Avenue"
        }
    )

    assert len(results) == 1
    assert results[0]["estimated_value"] == 350000


def test_valuation_fields():

    provider = ValuationProvider()

    result = provider.fetch({})[0]

    assert "rental_estimate" in result
    assert "confidence_score" in result
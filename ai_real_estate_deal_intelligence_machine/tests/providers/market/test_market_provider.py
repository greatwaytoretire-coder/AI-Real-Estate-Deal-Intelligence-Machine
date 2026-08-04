from ai_real_estate_deal_intelligence_machine.providers.market.market_provider import (
    MarketProvider,
)


def test_market_provider_config():

    provider = MarketProvider()

    config = provider.get_config()

    assert config.name == "market_provider"



def test_market_provider_fetch():

    provider = MarketProvider()

    results = provider.fetch(
        {
            "market": "Phoenix"
        }
    )

    assert len(results) == 1
    assert results[0]["market"] == "Phoenix"



def test_market_snapshot_fields():

    provider = MarketProvider()

    result = provider.fetch({})[0]

    assert "median_price" in result
    assert "investor_score" in result
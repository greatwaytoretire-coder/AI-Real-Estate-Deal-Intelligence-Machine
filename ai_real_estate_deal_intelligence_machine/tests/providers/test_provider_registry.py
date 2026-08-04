from ai_real_estate_deal_intelligence_machine.providers.provider_registry import (
    ProviderRegistry,
)

from ai_real_estate_deal_intelligence_machine.providers.mock_providers import (
    MockPropertyProvider,
    MockMarketProvider,
)

from ai_real_estate_deal_intelligence_machine.providers.provider_types import (
    ProviderStatus,
)


def test_register_property_provider():

    registry = ProviderRegistry()

    provider = MockPropertyProvider()

    registry.register_provider(provider)

    providers = registry.list_providers()

    assert "mock_property_feed" in providers



def test_get_registered_provider():

    registry = ProviderRegistry()

    provider = MockMarketProvider()

    registry.register_provider(provider)

    result = registry.get_provider(
        "mock_market_feed"
    )

    assert result.get_config().name == "mock_market_feed"



def test_provider_status():

    registry = ProviderRegistry()

    provider = MockPropertyProvider()

    registry.register_provider(
        provider,
        status=ProviderStatus.MOCK,
    )

    status = registry.get_status(
        "mock_property_feed"
    )

    assert status == ProviderStatus.MOCK



def test_missing_provider():

    registry = ProviderRegistry()

    try:

        registry.get_provider(
            "does_not_exist"
        )

        assert False

    except KeyError:

        assert True
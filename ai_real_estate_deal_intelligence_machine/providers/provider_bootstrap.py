from ai_real_estate_deal_intelligence_machine.providers.provider_registry import (
    ProviderRegistry,
)

from ai_real_estate_deal_intelligence_machine.providers.mock_providers import (
    MockPropertyProvider,
    MockMarketProvider,
    MockBuyerProvider,
    MockAttomProvider,
)

from ai_real_estate_deal_intelligence_machine.providers.provider_types import (
    ProviderStatus,
)


def create_provider_registry() -> ProviderRegistry:
    """
    Creates the default intelligence provider registry.

    Future live providers will be added here:
    - MLS APIs
    - County Records APIs
    - Market Data APIs
    - Listing Providers
    """

    registry = ProviderRegistry()

    registry.register_provider(
        MockPropertyProvider(),
        status=ProviderStatus.MOCK,
    )

    registry.register_provider(
        MockMarketProvider(),
        status=ProviderStatus.MOCK,
    )

    registry.register_provider(
        MockBuyerProvider(),
        status=ProviderStatus.MOCK,
    )

    registry.register_provider(
        MockAttomProvider(),
        status=ProviderStatus.MOCK,
    )

    return registry
from __future__ import annotations

from typing import Dict, List

from .providers.mock_providers import MockBuyerProvider, MockMarketProvider, MockPropertyProvider


class ProviderRegistry:
    """Phase 0 provider registry using local mock providers only."""

    def __init__(self) -> None:
        self._providers = [
            MockPropertyProvider(),
            MockMarketProvider(),
            MockBuyerProvider(),
        ]

    def enabled_providers(self) -> List[Dict[str, str]]:
        return [
            {
                "name": provider.record.name,
                "label": provider.record.label,
                "source_type": provider.record.source_type,
                "enabled": str(provider.record.enabled).lower(),
            }
            for provider in self._providers
        ]

    def fetch_all(self) -> List[Dict[str, str]]:
        all_data: List[Dict[str, str]] = []
        for provider in self._providers:
            for item in provider.fetch():
                payload = dict(item)
                payload["provider"] = provider.record.name
                all_data.append(payload)
        return all_data

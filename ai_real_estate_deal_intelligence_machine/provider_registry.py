from __future__ import annotations

from typing import Dict, List

from .db_client import DatabaseClient
from .providers.mock_providers import MockBuyerProvider, MockMarketProvider, MockPropertyProvider


class ProviderRegistry:
    """Phase 0 provider registry using local mock providers only."""

    def __init__(self, db_client: DatabaseClient = None) -> None:
        # If no db_client is provided, create a temporary one for backward compatibility with old tests.
        self._db_client = db_client or DatabaseClient()
        self._db_client.upsert_provider("mock_property_feed", "Mock Property Feed", "mock")
        self._db_client.upsert_provider("mock_market_feed", "Mock Market Feed", "mock")
        self._db_client.upsert_provider("mock_buyer_feed", "Mock Buyer Feed", "mock")

        self._providers = [
            MockPropertyProvider(),
            MockMarketProvider(),
            MockBuyerProvider(),
        ]


    def enabled_providers(self) -> List[Dict[str, str]]:
        providers = self._db_client.list_providers()
        return [p for p in providers if p["enabled"]]

    def fetch_all(self) -> List[Dict[str, str]]:
        all_data: List[Dict[str, str]] = []
        for provider in self._providers:
            for item in provider.fetch():
                payload = dict(item)
                payload["provider"] = provider.record.name
                all_data.append(payload)
        return all_data

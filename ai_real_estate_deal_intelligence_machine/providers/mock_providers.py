from __future__ import annotations

from typing import Any, Dict, List

from .base import DataProvider, ProviderConfig
from ..phase24 import DataSourceType


class MockPropertyProvider(DataProvider):
    def get_config(self) -> ProviderConfig:
        return ProviderConfig(
            name="mock_property_feed",
            label="Mock Property Feed",
            source_type=DataSourceType.MOCK,
        )

    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": "prop-001",
                "market": "Phoenix",
                "address": "101 Mock Street",
                "price": 215000,
                "opportunity_score": 82,
                "source_type": "mock",
            }
        ]


class MockMarketProvider(DataProvider):
    def get_config(self) -> ProviderConfig:
        return ProviderConfig(
            name="mock_market_feed",
            label="Mock Market Feed",
            source_type=DataSourceType.MOCK,
        )

    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "market": "Phoenix",
                "score": 87,
                "confidence": 0.91,
                "source_type": "mock",
            }
        ]


class MockBuyerProvider(DataProvider):
    def get_config(self) -> ProviderConfig:
        return ProviderConfig(
            name="mock_buyer_feed",
            label="Mock Buyer Feed",
            source_type=DataSourceType.MOCK,
        )

    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "buyer_name": "Mock Buyer Alpha",
                "demand_score": 88,
                "reliability_score": 90,
                "source_type": "mock",
            }
        ]


class MockAttomProvider(DataProvider):
    """Mock provider for ATTOM data, used for fallback and testing."""

    def get_config(self) -> ProviderConfig:
        return ProviderConfig(
            name="attom_mock", label="ATTOM API (Mock)", source_type=DataSourceType.MOCK
        )

    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"address": "123 Mock St", "attom_id": "12345", "source": "mock"}]

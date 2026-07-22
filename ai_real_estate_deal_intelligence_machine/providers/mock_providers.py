from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseProvider, ProviderRecord


class MockPropertyProvider(BaseProvider):
    @property
    def record(self) -> ProviderRecord:
        return ProviderRecord(
            name="mock_property_feed",
            label="Mock Property Feed",
            source_type="mock",
            enabled=True,
        )

    def fetch(self) -> List[Dict[str, Any]]:
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


class MockMarketProvider(BaseProvider):
    @property
    def record(self) -> ProviderRecord:
        return ProviderRecord(
            name="mock_market_feed",
            label="Mock Market Feed",
            source_type="mock",
            enabled=True,
        )

    def fetch(self) -> List[Dict[str, Any]]:
        return [
            {
                "market": "Phoenix",
                "score": 87,
                "confidence": 0.91,
                "source_type": "mock",
            }
        ]


class MockBuyerProvider(BaseProvider):
    @property
    def record(self) -> ProviderRecord:
        return ProviderRecord(
            name="mock_buyer_feed",
            label="Mock Buyer Feed",
            source_type="mock",
            enabled=True,
        )

    def fetch(self) -> List[Dict[str, Any]]:
        return [
            {
                "buyer_name": "Mock Buyer Alpha",
                "demand_score": 88,
                "reliability_score": 90,
                "source_type": "mock",
            }
        ]

"""Phase 0: Mission Control foundation with mock providers only.

This module intentionally provides a lightweight, production-minded skeleton
for the initial dashboard experience. It uses mock providers and clearly labels
all data sources to avoid misrepresenting mock data as live production data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class MockProvider:
    name: str
    label: str
    source_type: str = "mock"


class MockProviderRegistry:
    """Registry for mock-only provider integrations used during Phase 0."""

    def __init__(self) -> None:
        self._providers: List[MockProvider] = [
            MockProvider(name="mock_property_feed", label="Mock Property Feed"),
            MockProvider(name="mock_market_feed", label="Mock Market Feed"),
            MockProvider(name="mock_buyer_feed", label="Mock Buyer Feed"),
        ]

    def enabled_providers(self) -> List[Dict[str, str]]:
        return [
            {"name": provider.name, "label": provider.label, "source_type": provider.source_type}
            for provider in self._providers
        ]


class MissionControlDashboard:
    """Simple Phase 0 mission control summary for the AI Deal Machine."""

    def __init__(self) -> None:
        self._registry = MockProviderRegistry()

    def summary(self) -> Dict[str, int | str]:
        providers = self._registry.enabled_providers()

        return {
            "machine_status": "ONLINE",
            "markets_monitored": 5,
            "new_properties_discovered": 12,
            "new_buyers_discovered": 4,
            "deals_analyzed": 9,
            "high_priority_opportunities": 3,
            "seller_conversations": 2,
            "buyer_matches": 6,
            "active_deal_pipelines": 7,
            "pending_exceptions": 1,
            "deal_rooms_generated": 2,
            "completed_transactions": 0,
            "machine_performance": f"{len(providers)} mock providers active",
        }

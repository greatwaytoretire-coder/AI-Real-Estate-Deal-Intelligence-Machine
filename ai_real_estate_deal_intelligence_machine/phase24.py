from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class DataSourceType(str, Enum):
    """Enumeration for data source classifications."""

    MOCK = "MOCK"
    TEST = "TEST"
    LIVE = "LIVE"


@dataclass
class PilotDataRecord:
    """A wrapper for any data point, clarifying its source and confidence."""

    data: Any
    source: DataSourceType
    confidence: float
    source_label: str


@dataclass
class MarketPilotConfig:
    """Configuration for a single-market real-world pilot."""

    # Market Definition
    market_name: str
    state: str
    county: str
    target_zip_codes: List[str]

    # Property Strategy
    property_types: List[str]
    min_price: int
    max_price: int
    min_equity_percent: float
    max_repair_budget: int

    # Deal Criteria
    min_deal_score: float

    # Target Profiles
    target_seller_signals: List[str] = field(default_factory=list)
    target_buyer_criteria: Dict[str, Any] = field(default_factory=dict)


class PilotDashboard:
    """Generates a summary report for the configured market pilot."""

    def __init__(self, config: MarketPilotConfig):
        self.config = config

    def run_mock_pilot_summary(self) -> Dict[str, Any]:
        """
        Simulates running the pilot and generates a dashboard report.
        In a real system, this would query live, processed data.
        """
        # Simulate discovering opportunities that match the pilot config
        discovered_opportunities = [
            PilotDataRecord(
                data={"address": "123 Pilot St, Austin, TX 78704", "price": 450000},
                source=DataSourceType.LIVE,
                confidence=0.92,
                source_label="authorized-mls-feed-austin",
            ),
            PilotDataRecord(
                data={"address": "456 Test Ave, Austin, TX 78702", "price": 380000},
                source=DataSourceType.TEST,
                confidence=0.99,
                source_label="internal-test-data-set-v2",
            ),
            PilotDataRecord(
                data={"address": "789 Mockingbird Ln, Austin, TX 78701", "price": 510000},
                source=DataSourceType.MOCK,
                confidence=1.0,
                source_label="phase23-simulation-mock-data",
            ),
        ]

        # Filter opportunities based on config
        analyzed_opportunities = [
            op for op in discovered_opportunities if op.data["price"] <= self.config.max_price
        ]

        top_ranked_deals = [
            {
                "address": analyzed_opportunities[0].data["address"],
                "deal_score": 91.5,
                "data_source": analyzed_opportunities[0].source.value,
                "confidence": analyzed_opportunities[0].confidence,
            }
        ]

        buyer_matches = [
            {"buyer_id": "buyer-live-007", "match_score": 95.2, "criteria": self.config.target_buyer_criteria}
        ]

        return {
            "pilot_market": self.config.market_name,
            "target_zips": self.config.target_zip_codes,
            "market_heat_score": 8.1,  # Mocked score
            "opportunities_discovered": len(discovered_opportunities),
            "opportunities_analyzed": len(analyzed_opportunities),
            "top_ranked_deals": top_ranked_deals,
            "buyer_matches": buyer_matches,
            "data_sources_in_use": list(set(op.source.value for op in discovered_opportunities)),
            "report_status": "OK (SIMULATED DATA)",
        }
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .phase30 import CanonicalProperty, ContinuousRuntime


@dataclass
class LivePilotConfig:
    """Configuration for a single-market live pilot run."""

    # Geographic Filters
    market_name: str
    state: str
    target_zip_codes: List[str]

    # Property Criteria
    property_types: List[str]
    min_price: int
    max_price: int
    min_sqft: int = 500
    min_bedrooms: int = 2

    # Deal Criteria
    min_estimated_profit: float = 10000.0
    min_deal_score: float = 70.0
    investment_strategy: str = "Fix and Flip"


@dataclass
class RankedOpportunity:
    """A ranked opportunity ready for the pilot report."""

    canonical_id: str
    address: str
    deal_score: float
    confidence: float
    data_source: str
    warnings: List[str] = field(default_factory=list)
    missing_data: List[str] = field(default_factory=list)


@dataclass
class PilotReport:
    """A comprehensive report of the one-market pilot run."""

    config: LivePilotConfig
    opportunities_processed: int = 0
    opportunities_rejected: int = 0
    top_ranked_opportunities: List[RankedOpportunity] = field(default_factory=list)
    market_ranking: Dict[str, int] = field(default_factory=dict)  # e.g., {"78704": 10, "78701": 5}
    data_mode: str = "MOCK"  # MOCK or LIVE
    limitations: List[str] = field(default_factory=list)


class MarketRankingEngine:
    """Generates heat-map-ready rankings for sub-areas within a market."""

    def rank_by_zip(self, opportunities: List[CanonicalProperty]) -> Dict[str, int]:
        """Ranks ZIP codes by the volume of opportunities."""
        zip_counts: Dict[str, int] = {}
        for opp in opportunities:
            zip_counts[opp.zip_code] = zip_counts.get(opp.zip_code, 0) + 1
        return dict(sorted(zip_counts.items(), key=lambda item: item, reverse=True))


class LivePilotRunner:
    """Orchestrates a controlled, one-market live pilot."""

    def __init__(self, config: LivePilotConfig, runtime: ContinuousRuntime):
        self.config = config
        self.runtime = runtime
        self.ranking_engine = MarketRankingEngine()

    def _filter_opportunities(self, opportunities: List[CanonicalProperty]) -> tuple[List[CanonicalProperty], List[CanonicalProperty]]:
        """Applies the pilot configuration to filter opportunities."""
        accepted = []
        rejected = []
        for opp in opportunities:
            # For this simulation, we assume price/type are available on the canonical record.
            # In a real system, this might require an enrichment step first.
            if opp.zip_code not in self.config.target_zip_codes:
                rejected.append(opp)
                continue
            # Add other property criteria checks here (price, sqft, etc.)
            accepted.append(opp)
        return accepted, rejected

    def run(self, all_opportunities: List[CanonicalProperty]) -> PilotReport:
        """Executes the pilot workflow and generates a report."""
        report = PilotReport(config=self.config, data_mode=self.runtime.mode.value)

        # 1. Filter opportunities based on pilot configuration
        accepted_opportunities, rejected_opportunities = self._filter_opportunities(all_opportunities)
        report.opportunities_rejected = len(rejected_opportunities)

        processed_deals: List[RankedOpportunity] = []

        # 2. Process accepted opportunities through the AI pipeline
        for opp in accepted_opportunities:
            # In a real system, we'd create and monitor jobs. Here, we simulate the outcome.
            report.opportunities_processed += 1
            # Simulate a deal score and other metrics from the AI pipeline
            processed_deals.append(
                RankedOpportunity(
                    canonical_id=opp.canonical_id,
                    address=opp.address,
                    deal_score=85.5 if "123 main" in opp.address else 75.0,
                    confidence=0.9,
                    data_source=opp.source_provider,
                )
            )

        # 3. Rank the processed deals
        report.top_ranked_opportunities = sorted(processed_deals, key=lambda d: d.deal_score, reverse=True)

        # 4. Generate market rankings (heat map)
        report.market_ranking = self.ranking_engine.rank_by_zip(accepted_opportunities)

        return report
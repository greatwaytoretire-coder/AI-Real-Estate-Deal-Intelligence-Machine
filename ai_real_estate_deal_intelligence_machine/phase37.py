from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .phase29 import ScalingManager
from .phase30 import ContinuousRuntime


@dataclass
class MultiMarketReport:
    """A report summarizing a multi-market processing run."""

    markets_processed: List[str] = field(default_factory=list)
    markets_skipped_paused: List[str] = field(default_factory=list)
    markets_skipped_over_budget: List[str] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)


class MultiMarketOrchestrator:
    """
    Phase 37: Safely orchestrates processing across multiple configured markets.
    """

    def __init__(self, scaling_manager: ScalingManager, runtime: ContinuousRuntime):
        self.scaling_manager = scaling_manager
        self.runtime = runtime

    def run_all_active_markets(self, query: Dict[str, Any]) -> MultiMarketReport:
        """Iterates through all markets and runs ingestion for active ones within budget."""
        report = MultiMarketReport()
        active_markets = self.scaling_manager.get_active_markets()

        for market in active_markets:
            if not self.scaling_manager.is_within_budget(market.market_id):
                report.markets_skipped_over_budget.append(market.market_id)
                continue

            self.runtime.run_ingestion_for_market(market.market_id, query)
            report.markets_processed.append(market.market_id)

        return report
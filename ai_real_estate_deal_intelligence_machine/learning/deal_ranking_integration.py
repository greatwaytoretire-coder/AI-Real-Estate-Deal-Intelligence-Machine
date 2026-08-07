from __future__ import annotations

from typing import Any, Dict, List

from ai_real_estate_deal_intelligence_machine.learning.deal_ranking_engine import (
    DealRankingEngine,
)

from ai_real_estate_deal_intelligence_machine.learning.deal_priority_engine import (
    DealPriorityEngine,
)


class DealRankingIntegration:
    """
    Connects deal ranking and priority decision intelligence.

    Sprint 4 Part 13:
    Autonomous Deal Ranking Intelligence.
    """

    def __init__(self) -> None:
        self.ranking_engine = DealRankingEngine()
        self.priority_engine = DealPriorityEngine()


    def evaluate(
        self,
        deals: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Rank opportunities and generate priority actions.
        """

        ranking_result = (
            self.ranking_engine.rank(
                deals
            )
        )


        ranked_deals = (
            ranking_result[
                "ranked_deals"
            ]
        )


        priority_result = (
            self.priority_engine.prioritize(
                ranked_deals
            )
        )


        return {
            "ranking_result": ranking_result,

            "priority_result": priority_result,

            "status":
                "DEAL_RANKING_INTEGRATION_COMPLETE",
        }
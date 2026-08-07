from __future__ import annotations

from typing import Any, Dict, List


class DealRankingEngine:
    """
    Ranks investment opportunities based on
    predictive intelligence signals.

    Sprint 4 Part 13:
    Autonomous Deal Ranking Intelligence.
    """

    def rank(
        self,
        deals: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Rank multiple opportunities.

        Ranking factors:

        Deal Score          30%
        Market Confidence   20%
        Seller Motivation   20%
        Buyer Demand        15%
        Profit Margin       15%
        """

        ranked_deals = []

        for deal in deals:

            deal_score = float(
                deal.get(
                    "deal_score",
                    0,
                )
            )

            market_confidence = float(
                deal.get(
                    "market_confidence",
                    0,
                )
            )

            seller_motivation = float(
                deal.get(
                    "seller_motivation",
                    0,
                )
            )

            buyer_demand = float(
                deal.get(
                    "buyer_demand",
                    0,
                )
            )

            profit_margin = float(
                deal.get(
                    "profit_margin",
                    0,
                )
            )

            risk_level = deal.get(
                "risk_level",
                "MEDIUM",
            )


            risk_penalty = {
                "LOW": 0,
                "MEDIUM": 10,
                "HIGH": 20,
            }.get(
                risk_level,
                10,
            )


            ranking_score = (
                (deal_score * .30)
                +
                (market_confidence * .20)
                +
                (seller_motivation * .20)
                +
                (buyer_demand * .15)
                +
                (profit_margin * .15)
                -
                risk_penalty
            )


            if ranking_score >= 80:
                priority = "HIGH"

                recommendation = (
                    "IMMEDIATE_ACTION"
                )

            elif ranking_score >= 60:
                priority = "MEDIUM"

                recommendation = (
                    "FURTHER_ANALYSIS"
                )

            else:
                priority = "LOW"

                recommendation = (
                    "MONITOR"
                )


            ranked_deals.append(
                {
                    "deal_id": deal.get(
                        "deal_id"
                    ),

                    "ranking_score": round(
                        ranking_score,
                        2,
                    ),

                    "priority": priority,

                    "recommendation": (
                        recommendation
                    ),

                    "risk_level": risk_level,

                }
            )


        ranked_deals.sort(
            key=lambda x: x[
                "ranking_score"
            ],
            reverse=True,
        )


        return {
            "total_deals": len(
                ranked_deals
            ),

            "ranked_deals": ranked_deals,

            "top_deal": (
                ranked_deals[0]
                if ranked_deals
                else None
            ),

            "status":
                "DEALS_RANKED",
        }
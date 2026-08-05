from __future__ import annotations

from typing import Any, Dict, List

from .matching_models import BuyerMatch


class BuyerMatchingEngine:
    """
    Matches buyers to deals using simple scoring logic.

    This serves as the foundation for future AI-driven buyer ranking.
    """

    def match(
        self,
        buyers: List[Dict[str, Any]],
        deal: Dict[str, Any],
    ) -> List[BuyerMatch]:

        results: List[BuyerMatch] = []

        for buyer in buyers:

            score = 0
            reasoning: List[str] = []

            if deal["market"] in buyer.get("preferred_markets", []):
                score += 50
                reasoning.append("Market preference matched")

            if (
                deal["property_type"]
                in buyer.get("preferred_property_types", [])
            ):
                score += 30
                reasoning.append("Property type matched")

            investment_score = buyer.get(
                "investment_score",
                0,
            )

            score += investment_score * 0.2

            reasoning.append(
                f"Investment score contributed {investment_score * 0.2:.1f} points"
            )

            recommendation = (
                "MATCH"
                if score >= 70
                else "REVIEW"
            )

            results.append(
                BuyerMatch(
                    buyer_id=buyer["buyer_id"],
                    buyer_name=buyer["buyer_name"],
                    score=score,
                    recommendation=recommendation,
                    reasoning=reasoning,
                )
            )

        results.sort(
            key=lambda match: match.score,
            reverse=True,
        )

        return results
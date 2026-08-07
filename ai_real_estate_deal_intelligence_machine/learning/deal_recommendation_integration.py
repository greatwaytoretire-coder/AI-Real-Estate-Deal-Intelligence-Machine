from __future__ import annotations

from typing import Any, Dict, Iterable, List

from ai_real_estate_deal_intelligence_machine.learning.deal_recommendation_engine import (
    DealRecommendationEngine,
)

from ai_real_estate_deal_intelligence_machine.learning.recommendation_confidence_engine import (
    RecommendationConfidenceEngine,
)


class DealRecommendationIntegration:
    """
    Integrates recommendation generation and confidence evaluation.

    Sprint 4 Part 14:
    Deal Recommendation Intelligence.

    Flow:

        Deal Intelligence
              |
              v
        Deal Recommendation
              |
              v
        Recommendation Confidence
              |
              v
        Final Investment Decision
    """

    def __init__(self) -> None:
        self.recommendation_engine = (
            DealRecommendationEngine()
        )

        self.confidence_engine = (
            RecommendationConfidenceEngine()
        )

    def evaluate(
        self,
        deals: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluate multiple investment opportunities.

        Invalid records are ignored safely.
        """

        recommendations: List[Dict[str, Any]] = []

        for deal in deals:
            if not isinstance(deal, dict):
                continue

            recommendation = (
                self.recommendation_engine.recommend(
                    deal
                )
            )

            confidence = (
                self.confidence_engine.evaluate(
                    recommendation
                )
            )

            combined = {
                **recommendation,
                "confidence_score": confidence[
                    "confidence_score"
                ],
                "confidence_level": confidence[
                    "confidence_level"
                ],
            }

            recommendations.append(
                combined
            )

        recommendations.sort(
            key=lambda item: (
                item["confidence_score"],
                item["recommendation_score"],
            ),
            reverse=True,
        )

        top_recommendation = (
            recommendations[0]
            if recommendations
            else None
        )

        return {
            "total_deals": len(
                recommendations
            ),
            "recommendations": recommendations,
            "top_recommendation": (
                top_recommendation
            ),
            "status": (
                "DEAL_RECOMMENDATIONS_COMPLETE"
            ),
        }
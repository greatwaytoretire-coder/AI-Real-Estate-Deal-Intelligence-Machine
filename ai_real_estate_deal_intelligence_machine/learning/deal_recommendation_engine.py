from __future__ import annotations

from typing import Any, Dict


class DealRecommendationEngine:
    """
    Converts deal intelligence signals into an actionable
    investment recommendation.

    Sprint 4 Part 14:
    Deal Recommendation Intelligence.

    The engine considers:

    - Ranking score
    - Priority action
    - Predictive success probability
    - Market confidence
    - Risk level
    """

    def recommend(
        self,
        deal: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate an investment recommendation for a deal.
        """

        ranking_score = float(
            deal.get(
                "ranking_score",
                0.0,
            )
        )

        priority_action = str(
            deal.get(
                "priority_action",
                "IGNORE",
            )
        )

        success_probability = float(
            deal.get(
                "success_probability",
                0.0,
            )
        )

        market_confidence = float(
            deal.get(
                "market_confidence",
                0.0,
            )
        )

        risk_level = str(
            deal.get(
                "risk_level",
                "MEDIUM",
            )
        ).upper()

        # ---------------------------------------------------------
        # Risk adjustment
        # ---------------------------------------------------------

        risk_penalty = {
            "LOW": 0,
            "MEDIUM": 10,
            "HIGH": 20,
        }.get(
            risk_level,
            10,
        )

        # ---------------------------------------------------------
        # Recommendation score
        # ---------------------------------------------------------

        recommendation_score = (
            (ranking_score * 0.40)
            + (success_probability * 0.30)
            + (market_confidence * 0.20)
            + (
                (
                    100
                    if priority_action == "ACQUIRE_NOW"
                    else 75
                    if priority_action == "ANALYZE_NEXT"
                    else 50
                    if priority_action == "WATCH"
                    else 25
                )
                * 0.10
            )
            - risk_penalty
        )

        recommendation_score = max(
            0.0,
            min(
                100.0,
                recommendation_score,
            ),
        )

        # ---------------------------------------------------------
        # Recommendation decision
        # ---------------------------------------------------------

        if (
            recommendation_score >= 75
            and risk_level == "LOW"
        ):
            recommendation = "PURSUE"

        elif recommendation_score >= 60:
            recommendation = "REVIEW"

        else:
            recommendation = "PASS"

        # ---------------------------------------------------------
        # Confidence
        # ---------------------------------------------------------

        if recommendation_score >= 80:
            confidence = "HIGH"

        elif recommendation_score >= 60:
            confidence = "MEDIUM"

        else:
            confidence = "LOW"

        return {
            "deal_id": deal.get(
                "deal_id"
            ),
            "recommendation": recommendation,
            "recommendation_score": round(
                recommendation_score,
                2,
            ),
            "confidence": confidence,
            "ranking_score": round(
                ranking_score,
                2,
            ),
            "success_probability": round(
                success_probability,
                2,
            ),
            "market_confidence": round(
                market_confidence,
                2,
            ),
            "risk_level": risk_level,
            "priority_action": priority_action,
            "status": "RECOMMENDATION_GENERATED",
        }
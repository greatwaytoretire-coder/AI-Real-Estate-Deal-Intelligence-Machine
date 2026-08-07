from __future__ import annotations

from typing import Any, Dict


class RecommendationConfidenceEngine:
    """
    Evaluates confidence in an investment recommendation.

    Sprint 4 Part 14:
    Deal Recommendation Intelligence.

    Confidence is derived from:

    - Recommendation score
    - Predictive success probability
    - Market confidence
    - Risk level
    - Recommendation type
    """

    def evaluate(
        self,
        recommendation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate recommendation confidence.
        """

        recommendation_score = float(
            recommendation.get(
                "recommendation_score",
                0.0,
            )
        )

        success_probability = float(
            recommendation.get(
                "success_probability",
                0.0,
            )
        )

        market_confidence = float(
            recommendation.get(
                "market_confidence",
                0.0,
            )
        )

        risk_level = str(
            recommendation.get(
                "risk_level",
                "MEDIUM",
            )
        ).upper()

        recommendation_type = str(
            recommendation.get(
                "recommendation",
                "PASS",
            )
        ).upper()

        # ---------------------------------------------------------
        # Base confidence
        # ---------------------------------------------------------

        confidence_score = (
            (recommendation_score * 0.50)
            + (success_probability * 0.30)
            + (market_confidence * 0.20)
        )

        # ---------------------------------------------------------
        # Risk adjustment
        # ---------------------------------------------------------

        if risk_level == "LOW":
            confidence_score += 5

        elif risk_level == "MEDIUM":
            confidence_score -= 5

        elif risk_level == "HIGH":
            confidence_score -= 15

        # ---------------------------------------------------------
        # Recommendation alignment
        # ---------------------------------------------------------

        if recommendation_type == "PURSUE":
            confidence_score += 5

        elif recommendation_type == "PASS":
            confidence_score += 2

        confidence_score = max(
            0.0,
            min(
                100.0,
                confidence_score,
            ),
        )

        # ---------------------------------------------------------
        # Confidence level
        # ---------------------------------------------------------

        if confidence_score >= 80:
            confidence_level = "HIGH"

        elif confidence_score >= 60:
            confidence_level = "MEDIUM"

        else:
            confidence_level = "LOW"

        return {
            "deal_id": recommendation.get(
                "deal_id"
            ),
            "recommendation": recommendation_type,
            "confidence_score": round(
                confidence_score,
                2,
            ),
            "confidence_level": confidence_level,
            "risk_level": risk_level,
            "status": "RECOMMENDATION_CONFIDENCE_EVALUATED",
        }
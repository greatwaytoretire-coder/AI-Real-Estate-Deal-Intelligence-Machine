from __future__ import annotations

from typing import Any, Dict, List

from .acquisition_models import AcquisitionDecision


class AcquisitionAgent:
    """
    Autonomous acquisition intelligence agent.

    Evaluates property intelligence and determines
    whether an opportunity should be pursued.
    """

    def analyze(
        self,
        property_data: Dict[str, Any],
        market_data: Dict[str, Any],
        valuation_data: Dict[str, Any],
    ) -> AcquisitionDecision:

        score = 0
        reasoning: List[str] = []

        price = property_data.get("price", 0)

        estimated_value = valuation_data.get(
            "estimated_value",
            0,
        )

        market_score = market_data.get(
            "market_score",
            0,
        )

        if estimated_value > price:
            score += 40
            reasoning.append(
                "Property appears below estimated market value"
            )

        if market_score >= 80:
            score += 30
            reasoning.append(
                "Strong market conditions detected"
            )

        if price > 0:
            score += 20
            reasoning.append(
                "Property contains investment potential"
            )

        recommendation = (
            "PURSUE"
            if score >= 70
            else "REVIEW"
        )

        return AcquisitionDecision(
            property_id="PROP-001",
            address=property_data.get(
                "address",
                "Unknown",
            ),
            deal_score=score,
            recommendation=recommendation,
            reasoning=reasoning,
        )
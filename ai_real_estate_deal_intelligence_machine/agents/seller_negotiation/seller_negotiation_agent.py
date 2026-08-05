from __future__ import annotations

from typing import Any, Dict, List

from .seller_negotiation_models import (
    SellerNegotiationDecision,
)


class SellerNegotiationAgent:
    """
    Autonomous seller negotiation intelligence agent.

    Evaluates seller motivation,
    distress signals, and negotiation strategy.
    """

    def analyze(
        self,
        seller_data: Dict[str, Any],
        property_data: Dict[str, Any],
    ) -> SellerNegotiationDecision:

        reasoning: List[str] = []

        motivation_score = float(
            seller_data.get(
                "motivation_score",
                0,
            )
        )

        distress_score = float(
            seller_data.get(
                "distress_score",
                0,
            )
        )

        urgency = "LOW"

        if motivation_score >= 70:
            urgency = "HIGH"
            reasoning.append(
                "Seller motivation indicates strong negotiation opportunity"
            )
        else:
            reasoning.append(
                "Seller motivation appears limited"
            )

        if distress_score >= 70:
            reasoning.append(
                "Property shows elevated distress indicators"
            )
        else:
            reasoning.append(
                "Limited distress signals detected"
            )

        if motivation_score >= 70 and distress_score >= 70:
            strategy = "AGGRESSIVE_NEGOTIATION"
        elif motivation_score >= 50:
            strategy = "MODERATE_NEGOTIATION"
        else:
            strategy = "RELATIONSHIP_BUILDING"

        reasoning.append(
            f"Recommended strategy: {strategy}"
        )

        estimated_value = float(
            property_data.get(
                "estimated_value",
                0,
            )
        )

        return SellerNegotiationDecision(
            property_id="PROP-001",
            seller_name=seller_data.get(
                "seller_name",
                "Unknown Seller",
            ),
            motivation_score=motivation_score,
            distress_score=distress_score,
            urgency_level=urgency,
            recommended_strategy=strategy,
            offer_range_low=estimated_value * 0.65,
            offer_range_high=estimated_value * 0.80,
            reasoning=reasoning,
        )
from __future__ import annotations

from typing import Dict

from ai_real_estate_deal_intelligence_machine.disposition.disposition_models import (
    DispositionRecommendation,
)


class DispositionEngine:
    """
    Evaluates the best exit strategy for an investment opportunity.
    """

    def recommend(
        self,
        property_data: Dict,
        deal_data: Dict,
        buyer_data: Dict,
    ) -> DispositionRecommendation:

        property_id = property_data.get(
            "property_id",
            "PROP-001",
        )

        address = property_data.get(
            "address",
            "Unknown Address",
        )

        assignment_fee = max(
            deal_data.get("arv", 0)
            - deal_data.get("purchase_price", 0)
            - deal_data.get("repair_costs", 0),
            0,
        )

        reasoning = []

        if assignment_fee > 25000:
            strategy = "WHOLESALE_ASSIGNMENT"
            buyer_type = "CASH_INVESTOR"

            reasoning.append(
                "Strong assignment spread supports wholesale disposition."
            )

        else:
            strategy = "BUY_AND_HOLD"
            buyer_type = "LONG_TERM_INVESTOR"

            reasoning.append(
                "Lower immediate spread suggests long-term hold strategy."
            )

        if buyer_data:
            reasoning.append(
                "Buyer intelligence data considered."
            )

        return DispositionRecommendation(
            property_id=property_id,
            address=address,
            recommended_strategy=strategy,
            target_buyer_type=buyer_type,
            estimated_assignment_fee=float(assignment_fee),
            confidence_score=0.85,
            reasoning=reasoning,
        )
from __future__ import annotations

from typing import Any, Dict, List

from .underwriting_models import UnderwritingDecision


class UnderwritingAgent:
    """
    Autonomous real estate underwriting agent.

    Evaluates investment economics and determines
    if a deal meets financial requirements.
    """

    def analyze(
        self,
        property_data: Dict[str, Any],
        valuation_data: Dict[str, Any],
        expense_data: Dict[str, Any] | None = None,
    ) -> UnderwritingDecision:

        if expense_data is None:
            expense_data = {}

        purchase_price = float(
            property_data.get("price", 0)
        )

        arv = float(
            valuation_data.get(
                "estimated_value",
                0,
            )
        )

        repair_costs = float(
            expense_data.get(
                "repair_costs",
                0,
            )
        )

        holding_costs = float(
            expense_data.get(
                "holding_costs",
                0,
            )
        )

        total_cost = (
            purchase_price
            + repair_costs
            + holding_costs
        )

        projected_profit = (
            arv - total_cost
        )

        roi_percentage = 0

        if total_cost > 0:
            roi_percentage = (
                projected_profit / total_cost
            ) * 100

        reasoning: List[str] = []

        if projected_profit > 0:
            reasoning.append(
                "Positive projected profit identified"
            )
        else:
            reasoning.append(
                "Projected profit is negative based on current assumptions"
            )

        if roi_percentage >= 15:
            reasoning.append(
                "ROI meets investment target"
            )
        else:
            reasoning.append(
                "ROI does not currently meet investment target"
            )

        if arv > purchase_price:
            reasoning.append(
                "Property value exceeds purchase price"
            )
        else:
            reasoning.append(
                "Purchase price exceeds estimated value"
            )

        recommendation = (
            "APPROVE"
            if roi_percentage >= 15
            else "REVIEW"
        )

        return UnderwritingDecision(
            property_id="PROP-001",
            address=property_data.get(
                "address",
                "Unknown",
            ),
            purchase_price=purchase_price,
            arv=arv,
            repair_costs=repair_costs,
            holding_costs=holding_costs,
            projected_profit=projected_profit,
            roi_percentage=roi_percentage,
            recommendation=recommendation,
            reasoning=reasoning,
        )
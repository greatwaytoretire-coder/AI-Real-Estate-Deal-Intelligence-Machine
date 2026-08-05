from __future__ import annotations

from typing import Any, Dict, List

from .buyer_intelligence_models import (
    BuyerIntelligenceDecision,
)


class BuyerIntelligenceAgent:
    """
    Autonomous buyer intelligence agent.

    Evaluates buyer profiles and determines
    deal compatibility.
    """

    def analyze(
        self,
        buyer_data: Dict[str, Any],
        deal_data: Dict[str, Any],
    ) -> BuyerIntelligenceDecision:

        reasoning: List[str] = []

        investment_score = float(
            buyer_data.get(
                "investment_score",
                0,
            )
        )

        buyer_type = buyer_data.get(
            "buyer_type",
            "Unknown",
        )

        markets = buyer_data.get(
            "preferred_markets",
            [],
        )

        property_types = buyer_data.get(
            "preferred_property_types",
            [],
        )

        deal_market = deal_data.get(
            "market",
            "",
        )

        deal_type = deal_data.get(
            "property_type",
            "",
        )

        match_score = 0

        if deal_market in markets:
            match_score += 50
            reasoning.append(
                "Buyer operates in target market"
            )
        else:
            reasoning.append(
                "Buyer market preference does not match"
            )

        if deal_type in property_types:
            match_score += 30
            reasoning.append(
                "Property type matches buyer strategy"
            )
        else:
            reasoning.append(
                "Property type mismatch detected"
            )

        if investment_score >= 80:
            match_score += 20
            reasoning.append(
                "Buyer has strong investment profile"
            )
        else:
            reasoning.append(
                "Buyer investment profile requires review"
            )

        if match_score >= 80:
            recommendation = "HIGH_PRIORITY_BUYER"
        elif match_score >= 50:
            recommendation = "POTENTIAL_BUYER"
        else:
            recommendation = "LOW_PRIORITY_BUYER"

        reasoning.append(
            f"Buyer recommendation: {recommendation}"
        )

        return BuyerIntelligenceDecision(
            buyer_id="BUYER-001",
            buyer_name=buyer_data.get(
                "buyer_name",
                "Unknown Buyer",
            ),
            buyer_type=buyer_type,
            preferred_markets=markets,
            preferred_property_types=property_types,
            investment_score=investment_score,
            deal_match_score=match_score,
            recommendation=recommendation,
            reasoning=reasoning,
        )
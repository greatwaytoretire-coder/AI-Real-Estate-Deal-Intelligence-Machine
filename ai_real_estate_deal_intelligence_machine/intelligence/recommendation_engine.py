from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalysisResult,
)


@dataclass
class AcquisitionRecommendation:
    property_id: str
    recommendation: str
    priority: str
    reasoning: list[str]


class RecommendationEngine:
    """
    Converts deal analysis into acquisition recommendations.
    """

    def generate(
        self,
        analysis: DealAnalysisResult,
    ) -> AcquisitionRecommendation:

        reasoning = []

        recommendation = "PASS"
        priority = "LOW"

        if analysis.deal_score >= 90:
            recommendation = "ACQUIRE"
            priority = "HIGH"

            reasoning.append(
                "Deal score indicates an exceptional opportunity."
            )

        elif analysis.deal_score >= 75:
            recommendation = "PURSUE"
            priority = "MEDIUM"

            reasoning.append(
                "Deal meets investment criteria."
            )

        elif analysis.deal_score >= 60:
            recommendation = "NEGOTIATE"
            priority = "MEDIUM"

            reasoning.append(
                "Deal may work with improved terms."
            )

        else:
            reasoning.append(
                "Deal does not currently meet investment requirements."
            )

        if analysis.projected_profit >= 50000:
            reasoning.append(
                "Projected profit exceeds $50,000."
            )

        if analysis.mao > 0:
            reasoning.append(
                "Maximum allowable offer has been calculated."
            )

        if analysis.profit_margin >= 30:
            reasoning.append(
                "Profit margin indicates strong upside."
            )

        return AcquisitionRecommendation(
            property_id=analysis.property_id,
            recommendation=recommendation,
            priority=priority,
            reasoning=reasoning,
        )
from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalysisResult,
)


@dataclass
class InvestorReport:
    property_id: str
    executive_summary: str
    recommended_action: str
    strengths: list[str]
    risks: list[str]


class ReportGenerator:

    def generate(
        self,
        analysis: DealAnalysisResult,
    ) -> InvestorReport:

        strengths = []
        risks = []

        if analysis.projected_profit >= 50000:
            strengths.append("Projected profit exceeds $50,000.")

        if analysis.deal_score >= 75:
            strengths.append("High investment score.")

        if analysis.mao > 0:
            strengths.append("Maximum Allowable Offer calculated.")

        if analysis.deal_score < 60:
            risks.append("Low investment score.")

        if analysis.projected_profit < 25000:
            risks.append("Projected profit is relatively low.")

        if analysis.investment_grade == "STRONG":
            action = "PURSUE"

        elif analysis.investment_grade == "AVERAGE":
            action = "NEGOTIATE"

        else:
            action = "PASS"

        summary = (
            f"{analysis.property_id} has a projected profit of "
            f"${analysis.projected_profit:,.0f} with a "
            f"{analysis.investment_grade.lower()} investment rating."
        )

        return InvestorReport(
            property_id=analysis.property_id,
            executive_summary=summary,
            recommended_action=action,
            strengths=strengths,
            risks=risks,
        )
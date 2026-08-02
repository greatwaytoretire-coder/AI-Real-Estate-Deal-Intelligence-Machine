from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_intelligence_coordinator import (
    DealIntelligenceCoordinator,
)


@dataclass
class InvestorReport:
    property_id: str
    executive_summary: str
    recommendation: str
    deal_score: float
    projected_profit: float
    profit_margin: float
    risk_level: str
    status: str


class InvestorReportGenerator:
    """
    Generates an investor-ready report from the
    Deal Intelligence Coordinator.
    """

    def __init__(self):

        self.coordinator = DealIntelligenceCoordinator()

    def generate(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> InvestorReport:

        package = self.coordinator.generate_package(
            property_id=property_id,
            purchase_price=purchase_price,
            estimated_value=estimated_value,
            repair_cost=repair_cost,
        )

        summary = (
            f"{package.recommendation} opportunity "
            f"with a projected profit of "
            f"${package.projected_profit:,.0f}."
        )

        return InvestorReport(
            property_id=package.property_id,
            executive_summary=summary,
            recommendation=package.recommendation,
            deal_score=package.deal_score,
            projected_profit=package.projected_profit,
            profit_margin=package.profit_margin,
            risk_level=package.risk_level,
            status="COMPLETED",
        )
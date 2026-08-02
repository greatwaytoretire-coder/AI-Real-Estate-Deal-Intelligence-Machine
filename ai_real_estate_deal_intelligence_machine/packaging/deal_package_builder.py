from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.reports.investor_report_generator import (
    InvestorReportGenerator,
)


@dataclass
class DealPackage:

    property_id: str
    executive_summary: str
    recommendation: str
    deal_score: float
    projected_profit: float
    profit_margin: float
    risk_level: str
    status: str



class DealPackageBuilder:
    """
    Creates a complete investor-ready deal package.

    Flow:

    Investor Report
          |
          v
    Deal Package
    """

    def __init__(self):

        self.report_generator = InvestorReportGenerator()


    def build(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> DealPackage:


        report = self.report_generator.generate(
            property_id=property_id,
            purchase_price=purchase_price,
            estimated_value=estimated_value,
            repair_cost=repair_cost,
        )


        return DealPackage(
            property_id=report.property_id,
            executive_summary=report.executive_summary,
            recommendation=report.recommendation,
            deal_score=report.deal_score,
            projected_profit=report.projected_profit,
            profit_margin=report.profit_margin,
            risk_level=report.risk_level,
            status="COMPLETED",
        )
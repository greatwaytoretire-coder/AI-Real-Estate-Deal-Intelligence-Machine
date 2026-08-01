from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
    DealAnalysisResult,
)

from ai_real_estate_deal_intelligence_machine.intelligence.report_generator import (
    ReportGenerator,
    InvestorReport,
)


@dataclass
class DealAnalysisResponse:
    analysis: DealAnalysisResult
    report: InvestorReport


class DealAnalysisService:

    def __init__(self):

        self.analyzer = DealAnalyzer()
        self.report_generator = ReportGenerator()


    def analyze(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> DealAnalysisResponse:

        analysis = self.analyzer.analyze(
            property_id=property_id,
            purchase_price=purchase_price,
            estimated_value=estimated_value,
            repair_cost=repair_cost,
        )

        report = self.report_generator.generate(
            analysis,
        )

        return DealAnalysisResponse(
            analysis=analysis,
            report=report,
        )
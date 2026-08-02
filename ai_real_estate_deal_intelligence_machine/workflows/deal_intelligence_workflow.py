from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
    DealAnalysisResult,
)

from ai_real_estate_deal_intelligence_machine.intelligence.report_generator import (
    ReportGenerator,
    InvestorReport,
)

from ai_real_estate_deal_intelligence_machine.intelligence.recommendation_engine import (
    RecommendationEngine,
)


@dataclass
class DealIntelligenceResult:
    analysis: DealAnalysisResult
    report: InvestorReport
    recommendation: object


class DealIntelligenceWorkflow:

    def __init__(self):

        self.analyzer = DealAnalyzer()

        self.report_generator = ReportGenerator()

        self.recommendation_engine = RecommendationEngine()


    def execute(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> DealIntelligenceResult:


        analysis = self.analyzer.analyze(
            property_id=property_id,
            purchase_price=purchase_price,
            estimated_value=estimated_value,
            repair_cost=repair_cost,
        )


        report = self.report_generator.generate(
            analysis
        )


        recommendation = (
            self.recommendation_engine.generate(
                analysis
            )
        )


        return DealIntelligenceResult(
            analysis=analysis,
            report=report,
            recommendation=recommendation,
        )
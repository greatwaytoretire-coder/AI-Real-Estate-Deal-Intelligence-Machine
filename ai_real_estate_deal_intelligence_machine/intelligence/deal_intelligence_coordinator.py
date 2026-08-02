from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
)

from ai_real_estate_deal_intelligence_machine.intelligence.recommendation_engine import (
    RecommendationEngine,
)

from ai_real_estate_deal_intelligence_machine.services.deal_analysis_service import (
    DealAnalysisService,
)


@dataclass
class DealIntelligencePackage:

    property_id: str

    deal_score: float

    recommendation: str

    priority: str

    reasoning: list[str]

    status: str



class DealIntelligenceCoordinator:
    """
    Coordinates the complete deal intelligence process.

    Flow:

    Deal Analysis
        ↓
    Recommendation
        ↓
    Intelligence Package
    """


    def __init__(self):

        self.deal_analyzer = DealAnalyzer()

        self.recommendation_engine = RecommendationEngine()

        self.deal_analysis_service = DealAnalysisService()



    def analyze(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> DealIntelligencePackage:


        analysis = self.deal_analyzer.analyze(
            property_id=property_id,
            purchase_price=purchase_price,
            estimated_value=estimated_value,
            repair_cost=repair_cost,
        )


        recommendation = (
            self.recommendation_engine.generate(
                analysis
            )
        )


        return DealIntelligencePackage(
            property_id=property_id,
            deal_score=analysis.deal_score,
            recommendation=(
                recommendation.recommendation
            ),
            priority=(
                recommendation.priority
            ),
            reasoning=(
                recommendation.reasoning
            ),
            status="COMPLETED",
        )
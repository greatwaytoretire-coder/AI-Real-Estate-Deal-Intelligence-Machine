from dataclasses import dataclass

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
)

from ai_real_estate_deal_intelligence_machine.intelligence.recommendation_engine import (
    RecommendationEngine,
)


@dataclass
class DealIntelligencePackage:

    property_id: str

    deal_score: float

    recommendation: str

    priority: str

    reasoning: list[str]

    purchase_price: float

    estimated_value: float

    repair_cost: float

    projected_profit: float

    mao: float

    profit_margin: float

    risk_level: str

    status: str



class DealIntelligenceCoordinator:
    """
    Coordinates complete deal intelligence.

    Flow:

    Deal Analysis
        ↓
    Recommendation
        ↓
    Risk Evaluation
        ↓
    Investor Intelligence Package
    """


    def __init__(self):

        self.deal_analyzer = DealAnalyzer()

        self.recommendation_engine = RecommendationEngine()



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


        recommendation = self.recommendation_engine.generate(
            analysis
        )


        risk_level = self.calculate_risk_level(
            analysis.deal_score,
            analysis.profit_margin,
        )


        return DealIntelligencePackage(

            property_id=property_id,

            deal_score=analysis.deal_score,

            recommendation=recommendation.recommendation,

            priority=recommendation.priority,

            reasoning=recommendation.reasoning,

            purchase_price=purchase_price,

            estimated_value=estimated_value,

            repair_cost=repair_cost,

            projected_profit=analysis.projected_profit,

            mao=analysis.mao,

            profit_margin=analysis.profit_margin,

            risk_level=risk_level,

            status="COMPLETED",
        )



    def generate_package(
        self,
        property_id: str,
        purchase_price: float,
        estimated_value: float,
        repair_cost: float,
    ) -> DealIntelligencePackage:

        return self.analyze(
            property_id=property_id,
            purchase_price=purchase_price,
            estimated_value=estimated_value,
            repair_cost=repair_cost,
        )



    def calculate_risk_level(
        self,
        deal_score: float,
        profit_margin: float,
    ) -> str:


        if deal_score >= 85 and profit_margin >= 35:
            return "LOW"


        if deal_score >= 70 and profit_margin >= 20:
            return "MEDIUM"


        return "HIGH"
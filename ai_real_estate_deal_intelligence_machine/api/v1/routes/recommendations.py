from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.recommendation import (
    RecommendationRequest,
)

from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
)

from ai_real_estate_deal_intelligence_machine.intelligence.recommendation_engine import (
    RecommendationEngine,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
)


@router.post("/generate")
def generate_recommendation(
    request: RecommendationRequest,
):

    analyzer = DealAnalyzer()

    analysis = analyzer.analyze(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )

    engine = RecommendationEngine()

    recommendation = engine.generate(
        analysis
    )

    return {
        "property_id": recommendation.property_id,
        "recommendation": recommendation.recommendation,
        "priority": recommendation.priority,
        "reasoning": recommendation.reasoning,
    }
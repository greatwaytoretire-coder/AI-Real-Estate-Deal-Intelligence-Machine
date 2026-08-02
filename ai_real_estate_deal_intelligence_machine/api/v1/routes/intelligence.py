from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.deal_analysis import (
    DealAnalysisRequest,
    DealAnalysisResponse,
)

from ai_real_estate_deal_intelligence_machine.services.deal_analysis_service import (
    DealAnalysisService,
)


router = APIRouter(
    prefix="/intelligence",
    tags=["Intelligence"],
)


@router.post(
    "/analyze",
    response_model=DealAnalysisResponse,
)
def analyze_deal(
    request: DealAnalysisRequest,
):

    service = DealAnalysisService()

    result = service.analyze(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )

    return DealAnalysisResponse(
        property_id=result.analysis.property_id,
        projected_profit=result.analysis.projected_profit,
        deal_score=result.analysis.deal_score,
        investment_grade=result.analysis.investment_grade,
        recommended_action=result.report.recommended_action,
        executive_summary=result.report.executive_summary,
        strengths=result.report.strengths,
        risks=result.report.risks,
    )
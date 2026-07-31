from fastapi import APIRouter, Depends

from ai_real_estate_deal_intelligence_machine.api.dependencies import (
    get_deal_service,
)

from ai_real_estate_deal_intelligence_machine.services.deal_service import (
    DealService,
)

from ..schemas.deal import (
    DealAnalysisRequest,
    DealAnalysisResponse,
)


router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)


@router.post(
    "/analyze",
    response_model=DealAnalysisResponse,
)
def analyze_deal(
    request: DealAnalysisRequest,
    service: DealService = Depends(get_deal_service),
):

    result = service.analyze_deal(
        request.model_dump()
    )

    return {
        "property_id": request.property_id,
        "analysis_status": result["analysis_status"],
    }
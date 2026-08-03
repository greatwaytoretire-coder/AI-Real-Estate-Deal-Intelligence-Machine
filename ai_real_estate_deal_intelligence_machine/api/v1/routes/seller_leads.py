from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.seller_lead import (
    SellerLeadRequest,
    SellerLeadResponse,
)

from ai_real_estate_deal_intelligence_machine.acquisition.seller_lead_pipeline import (
    SellerLeadPipeline,
)


router = APIRouter(
    prefix="/seller-leads",
    tags=["seller-leads"],
)


pipeline = SellerLeadPipeline()



@router.post(
    "/analyze",
    response_model=list[SellerLeadResponse],
)
def analyze_seller_lead(
    request: SellerLeadRequest,
):

    results = pipeline.analyze_lead(
        market=request.market,
        property_address=request.property_address,
        estimated_value=request.estimated_value,
        motivation_score=request.motivation_score,
        distress_signals=request.distress_signals,
    )


    return results
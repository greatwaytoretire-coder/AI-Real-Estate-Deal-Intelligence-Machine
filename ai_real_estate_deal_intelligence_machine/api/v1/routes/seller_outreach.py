from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.acquisition.seller_outreach_engine import (
    SellerOutreachEngine,
)
from ai_real_estate_deal_intelligence_machine.api.schemas.seller_outreach import (
    SellerOutreachRequest,
    SellerOutreachResponse,
)

router = APIRouter(
    prefix="/seller-outreach",
    tags=["Seller Outreach"],
)

engine = SellerOutreachEngine()


@router.post(
    "/generate",
    response_model=SellerOutreachResponse,
)
def generate_seller_outreach(
    request: SellerOutreachRequest,
) -> SellerOutreachResponse:

    package = engine.generate(
        seller_id=request.seller_id,
        property_id=request.property_id,
        motivation_level=request.motivation_level,
        preferred_channel=request.preferred_channel,
    )

    return SellerOutreachResponse(
        seller_id=package.seller_id,
        property_id=package.property_id,
        outreach_channel=package.outreach_channel,
        priority=package.priority,
        message=package.message,
        status=package.status,
    )
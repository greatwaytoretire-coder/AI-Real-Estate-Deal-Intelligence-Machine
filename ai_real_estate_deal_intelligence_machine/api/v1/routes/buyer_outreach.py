from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.buyer_outreach import (
    BuyerOutreachRequest,
    BuyerOutreachResponse,
)

from ai_real_estate_deal_intelligence_machine.disposition.buyer_outreach_engine import (
    BuyerOutreachEngine,
)


router = APIRouter(
    prefix="/buyer-outreach",
    tags=["Buyer Outreach"],
)


engine = BuyerOutreachEngine()



@router.post(
    "/generate",
    response_model=BuyerOutreachResponse,
)
def generate_buyer_outreach(
    request: BuyerOutreachRequest,
):

    package = engine.generate(
        property_id=request.property_id,
        buyer_id=request.buyer_id,
        buyer_type=request.buyer_type,
        preferred_channel=request.preferred_channel,
    )


    return BuyerOutreachResponse(

        property_id=package.property_id,

        buyer_id=package.buyer_id,

        outreach_channel=package.outreach_channel,

        priority=package.priority,

        message=package.message,

        status=package.status,

    )
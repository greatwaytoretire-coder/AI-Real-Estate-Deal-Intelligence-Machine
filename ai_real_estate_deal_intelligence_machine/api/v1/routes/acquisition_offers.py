from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.acquisition.offers.offer_generation_engine import (
    OfferGenerationEngine,
)

from ai_real_estate_deal_intelligence_machine.api.schemas.acquisition_offer import (
    AcquisitionOfferRequest,
    AcquisitionOfferResponse,
)


router = APIRouter(
    prefix="/acquisition-offers",
    tags=["Acquisition Offers"],
)


engine = OfferGenerationEngine()


@router.post(
    "/generate",
    response_model=AcquisitionOfferResponse,
)
def generate_acquisition_offer(
    request: AcquisitionOfferRequest,
):

    offer = engine.calculate_offer(
        property_id=request.property_id,
        arv=request.arv,
        repair_cost=request.repair_cost,
        desired_profit_margin=request.desired_profit_margin,
    )


    return AcquisitionOfferResponse(

        property_id=offer.property_id,

        arv=offer.arv,

        repair_cost=offer.repair_cost,

        recommended_offer=offer.recommended_offer,

        confidence_score=offer.confidence_score,

        reasoning=offer.reasoning,

    )
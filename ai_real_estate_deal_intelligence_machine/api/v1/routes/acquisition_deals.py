from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.acquisition.deals.acquisition_deal_manager import (
    AcquisitionDealManager,
    AcquisitionDealStatus,
)

from ai_real_estate_deal_intelligence_machine.api.schemas.acquisition_deal import (
    AcquisitionDealResponse,
    AcquisitionDealStatusRequest,
)



router = APIRouter(
    prefix="/acquisition-deals",
    tags=["Acquisition Deals"],
)



manager = AcquisitionDealManager()



@router.get(
    "",
    response_model=list[AcquisitionDealResponse],
)
def get_acquisition_deals():

    deals = manager.get_deals()

    return [

        AcquisitionDealResponse(
            deal_id=deal.deal_id,
            seller_id=deal.seller_id,
            property_address=deal.property_address,
            estimated_value=deal.estimated_value,
            repair_cost=deal.repair_cost,
            recommended_offer=deal.recommended_offer,
            status=deal.status.value,
            notes=deal.notes,
        )

        for deal in deals

    ]



@router.post(
    "/advance",
    response_model=AcquisitionDealResponse,
)
def advance_acquisition_deal(
    request: AcquisitionDealStatusRequest,
):

    updated = manager.advance_status(
        deal_id=request.deal_id,
        new_status=AcquisitionDealStatus(
            request.new_status
        ),
        note=request.note,
    )


    return AcquisitionDealResponse(

        deal_id=updated.deal_id,
        seller_id=updated.seller_id,
        property_address=updated.property_address,
        estimated_value=updated.estimated_value,
        repair_cost=updated.repair_cost,
        recommended_offer=updated.recommended_offer,
        status=updated.status.value,
        notes=updated.notes,

    )
from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.api.schemas.rent_collection import (
    RentPaymentCreateRequest,
)

from ai_real_estate_deal_intelligence_machine.rent_collection.rent_collection_engine import (
    RentCollectionEngine,
)


router = APIRouter()


engine = RentCollectionEngine()


@router.post("")
def create_rent_payment(
    request: RentPaymentCreateRequest,
):

    try:

        payment = engine.create_payment(
            payment_id=request.payment_id,
            tenant_id=request.tenant_id,
            property_id=request.property_id,
            amount=request.amount,
            payment_date=request.payment_date,
        )

        return payment


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("")
def get_rent_payments():

    return engine.get_payments()
from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.api.schemas.property_financials import (
    PropertyFinancialCreateRequest,
)

from ai_real_estate_deal_intelligence_machine.property_financials.property_financials_engine import (
    PropertyFinancialsEngine,
)


router = APIRouter()


engine = PropertyFinancialsEngine()


@router.post("")
def create_financial_record(
    request: PropertyFinancialCreateRequest,
):

    try:

        return engine.create_financial_record(
            record_id=request.record_id,
            property_id=request.property_id,
            income=request.income,
            expenses=request.expenses,
            period=request.period,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("")
def get_financial_records():

    return engine.get_financial_records()
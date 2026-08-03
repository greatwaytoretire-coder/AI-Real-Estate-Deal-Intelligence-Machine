from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.acquisition.closing.closing_management_engine import (
    ClosingManagementEngine,
)

from ai_real_estate_deal_intelligence_machine.api.schemas.closing import (
    ClosingCreate,
    ClosingResponse,
)


router = APIRouter(
    prefix="/closings",
    tags=["Closings"],
)


engine = ClosingManagementEngine()



@router.post(
    "",
    response_model=ClosingResponse,
)
def create_closing(
    request: ClosingCreate,
):

    closing = engine.create_closing(
        closing_id=request.closing_id,
        contract_id=request.contract_id,
        property_address=request.property_address,
        title_company=request.title_company,
        closing_date=request.closing_date,
    )

    return closing



@router.get(
    "",
    response_model=list[ClosingResponse],
)
def get_closings():

    return engine.get_closings()
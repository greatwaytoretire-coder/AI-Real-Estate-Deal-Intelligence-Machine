from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.acquisition.due_diligence.due_diligence_engine import (
    DueDiligenceEngine,
)

from ai_real_estate_deal_intelligence_machine.api.schemas.due_diligence import (
    DueDiligenceCreate,
    DueDiligenceResponse,
)


router = APIRouter(
    prefix="/due-diligence",
    tags=["Due Diligence"],
)


engine = DueDiligenceEngine()



@router.post(
    "",
    response_model=DueDiligenceResponse,
)
def create_due_diligence(
    request: DueDiligenceCreate,
):

    review = engine.create_review(
        review_id=request.review_id,
        property_address=request.property_address,
        contract_id=request.contract_id,
    )

    return review



@router.get(
    "",
    response_model=list[DueDiligenceResponse],
)
def get_due_diligence():

    return engine.get_reviews()
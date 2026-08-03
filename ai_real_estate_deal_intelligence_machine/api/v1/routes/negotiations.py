from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.acquisition.negotiations.negotiation_engine import (
    NegotiationEngine,
)

from ai_real_estate_deal_intelligence_machine.api.schemas.negotiation import (
    NegotiationAnalysisRequest,
    NegotiationAnalysisResponse,
)


router = APIRouter(
    prefix="/negotiations",
    tags=["Negotiations"],
)


engine = NegotiationEngine()


@router.post(
    "/analyze",
    response_model=NegotiationAnalysisResponse,
)
def analyze_negotiation(
    request: NegotiationAnalysisRequest,
):

    try:

        analysis = engine.analyze_negotiation(
            deal_id=request.deal_id,
            current_offer=request.current_offer,
            seller_counter_offer=request.seller_counter_offer,
            arv=request.arv,
        )


        return NegotiationAnalysisResponse(
            deal_id=analysis.deal_id,
            current_offer=analysis.current_offer,
            seller_counter_offer=analysis.seller_counter_offer,
            arv=analysis.arv,
            negotiation_stage=analysis.negotiation_stage.value,
            recommended_offer=analysis.recommended_offer,
            acceptance_probability=analysis.acceptance_probability,
            reasoning=analysis.reasoning,
        )


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )
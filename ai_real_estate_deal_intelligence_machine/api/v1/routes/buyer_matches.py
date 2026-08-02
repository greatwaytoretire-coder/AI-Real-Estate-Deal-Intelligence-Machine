from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.buyer_match import (
    BuyerMatchRequest,
    BuyerMatchResponse,
)

from ai_real_estate_deal_intelligence_machine.buyers.buyer_intelligence_engine import (
    BuyerIntelligenceEngine,
)


router = APIRouter(
    prefix="/buyer-matches",
    tags=["Buyer Matches"],
)


engine = BuyerIntelligenceEngine()


@router.post(
    "",
    response_model=list[BuyerMatchResponse],
)
def create_buyer_matches(
    request: BuyerMatchRequest,
):

    matches = engine.find_matches(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )


    return [

        BuyerMatchResponse(
            buyer_id=match.buyer_id,
            buyer_name=match.buyer_name,
            match_score=match.match_score,
            reasoning=match.reasoning,
        )

        for match in matches

    ]
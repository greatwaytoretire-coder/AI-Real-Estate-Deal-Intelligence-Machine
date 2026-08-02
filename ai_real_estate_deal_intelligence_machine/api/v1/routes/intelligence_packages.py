from fastapi import APIRouter


from ai_real_estate_deal_intelligence_machine.intelligence.deal_intelligence_coordinator import (
    DealIntelligenceCoordinator,
)


from ai_real_estate_deal_intelligence_machine.api.schemas.intelligence_package import (
    IntelligencePackageRequest,
    IntelligencePackageResponse,
)



router = APIRouter(
    prefix="/intelligence",
    tags=["intelligence"],
)



coordinator = DealIntelligenceCoordinator()



@router.post(
    "/package",
    response_model=IntelligencePackageResponse,
)
def create_intelligence_package(
    request: IntelligencePackageRequest,
):


    result = coordinator.analyze(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )


    return IntelligencePackageResponse(

        property_id=result.property_id,

        deal_score=result.deal_score,

        recommendation=result.recommendation,

        priority=result.priority,

        reasoning=result.reasoning,

        status=result.status,
    )
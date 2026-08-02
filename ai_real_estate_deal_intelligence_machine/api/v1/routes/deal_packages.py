from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.deal_package import (
    DealPackageRequest,
    DealPackageResponse,
)

from ai_real_estate_deal_intelligence_machine.packaging.deal_package_builder import (
    DealPackageBuilder,
)


router = APIRouter(
    prefix="/deal-packages",
    tags=["Deal Packages"],
)


builder = DealPackageBuilder()


@router.post(
    "/build",
    response_model=DealPackageResponse,
)
def build_deal_package(
    request: DealPackageRequest,
):

    package = builder.build(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )


    return DealPackageResponse(
        property_id=package.property_id,
        executive_summary=package.executive_summary,
        recommendation=package.recommendation,
        deal_score=package.deal_score,
        projected_profit=package.projected_profit,
        profit_margin=package.profit_margin,
        risk_level=package.risk_level,
        status=package.status,
    )
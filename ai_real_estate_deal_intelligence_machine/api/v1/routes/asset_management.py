from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.acquisition.post_closing.asset_management_engine import (
    AssetManagementEngine,
)

from ai_real_estate_deal_intelligence_machine.api.schemas.asset_management import (
    AssetCreateRequest,
)


router = APIRouter(
    prefix="/asset-management",
    tags=["Asset Management"],
)


engine = AssetManagementEngine()


@router.post("")
def create_asset(
    request: AssetCreateRequest,
):

    asset = engine.create_asset(
        asset_id=request.asset_id,
        property_address=request.property_address,
        acquisition_price=request.acquisition_price,
        closing_date=request.closing_date,
        strategy=request.strategy,
    )

    return asset



@router.get("")
def get_assets():

    return engine.get_assets()



@router.get("/{asset_id}/performance")
def get_asset_performance(
    asset_id: str,
):

    return engine.calculate_performance(
        asset_id
    )
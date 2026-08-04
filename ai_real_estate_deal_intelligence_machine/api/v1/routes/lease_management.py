from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.api.schemas.lease_management import (
    LeaseCreateRequest,
)

from ai_real_estate_deal_intelligence_machine.lease_management.lease_management_engine import (
    LeaseManagementEngine,
)

router = APIRouter()

engine = LeaseManagementEngine()


@router.post("")
def create_lease(request: LeaseCreateRequest):
    try:
        lease = engine.create_lease(
            lease_id=request.lease_id,
            tenant_id=request.tenant_id,
            property_id=request.property_id,
            start_date=request.start_date,
            end_date=request.end_date,
            monthly_rent=request.monthly_rent,
        )
        return lease

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("")
def get_leases():
    return engine.get_leases()
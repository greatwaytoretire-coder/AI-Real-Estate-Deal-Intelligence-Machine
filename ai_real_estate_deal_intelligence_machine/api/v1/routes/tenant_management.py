from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.api.schemas.tenant_management import (
    TenantCreateRequest,
    TenantStatusUpdateRequest,
)

from ai_real_estate_deal_intelligence_machine.property_management.tenant_management_engine import (
    TenantManagementEngine,
)


router = APIRouter(
    prefix="/tenant-management",
    tags=["Tenant Management"],
)


engine = TenantManagementEngine()


@router.post("")
def create_tenant(request: TenantCreateRequest):

    tenant = engine.create_tenant(
        tenant_id=request.tenant_id,
        property_id=request.property_id,
        tenant_name=request.tenant_name,
        monthly_rent=request.monthly_rent,
    )

    return tenant


@router.get("")
def get_tenants():

    return engine.get_tenants()


@router.patch("/{tenant_id}")
def update_tenant_status(
    tenant_id: str,
    request: TenantStatusUpdateRequest,
):

    try:
        return engine.update_status(
            tenant_id=tenant_id,
            status=request.status,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
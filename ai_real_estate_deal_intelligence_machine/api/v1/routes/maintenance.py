from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.api.schemas.maintenance import (
    MaintenanceRequest,
)

from ai_real_estate_deal_intelligence_machine.property_management.maintenance_management_engine import (
    MaintenanceManagementEngine,
    PriorityLevel,
)


router = APIRouter(
    prefix="/maintenance",
    tags=["maintenance"],
)


engine = MaintenanceManagementEngine()


@router.post("")
def create_maintenance(
    request: MaintenanceRequest,
):

    try:
        priority = PriorityLevel(
            request.priority
        )

    except ValueError:

        raise HTTPException(
            status_code=400,
            detail="Invalid maintenance priority.",
        )


    maintenance = engine.create_work_order(
        work_order_id=request.work_order_id,
        property_id=request.property_id,
        description=request.description,
        priority=priority,
        estimated_cost=request.estimated_cost,
    )


    return {
        "work_order_id": maintenance.work_order_id,
        "property_id": maintenance.property_id,
        "description": maintenance.description,
        "priority": maintenance.priority.value,
        "estimated_cost": maintenance.estimated_cost,
        "status": maintenance.status,
    }
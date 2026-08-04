from fastapi import APIRouter, HTTPException


from ai_real_estate_deal_intelligence_machine.api.schemas.inspection_management import (
    InspectionCreateRequest,
)


from ai_real_estate_deal_intelligence_machine.property_management.inspection_management.inspection_management_engine import (
    InspectionManagementEngine,
)



router = APIRouter()


engine = InspectionManagementEngine()



@router.post("")
def create_inspection(
    request: InspectionCreateRequest
):

    try:

        inspection = engine.create_inspection(
            inspection_id=request.inspection_id,
            property_id=request.property_id,
            inspector_name=request.inspector_name,
            inspection_date=request.inspection_date,
            condition=request.condition,
        )


        return inspection


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )



@router.get("")
def get_inspections():

    return engine.get_inspections()
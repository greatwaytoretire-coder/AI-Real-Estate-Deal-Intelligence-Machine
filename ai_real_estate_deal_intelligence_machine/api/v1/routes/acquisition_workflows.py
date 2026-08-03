from fastapi import APIRouter

from ...schemas.acquisition_workflow import (
    AcquisitionWorkflowRequest,
    AcquisitionWorkflowResponse,
)

from ....workflows.acquisition.acquisition_workflow_engine import (
    AcquisitionWorkflowEngine,
    AcquisitionStage,
)


router = APIRouter(
    prefix="/acquisition-workflows",
    tags=["Acquisition Workflows"],
)


engine = AcquisitionWorkflowEngine()



@router.get(
    "",
    response_model=list[AcquisitionWorkflowResponse],
)
def get_acquisition_workflows():

    workflows = engine.get_workflows()

    return [

        AcquisitionWorkflowResponse(
            seller_id=item.seller_id,
            property_address=item.property_address,
            current_stage=item.current_stage.value,
            offer_amount=item.offer_amount,
            notes=item.notes,
        )

        for item in workflows

    ]



@router.post(
    "/advance",
    response_model=AcquisitionWorkflowResponse,
)
def advance_acquisition_workflow(
    request: AcquisitionWorkflowRequest,
):

    workflow = engine.advance_stage(
        seller_id=request.seller_id,
        new_stage=AcquisitionStage(
            request.new_stage
        ),
        note=request.note,
    )


    return AcquisitionWorkflowResponse(

        seller_id=workflow.seller_id,

        property_address=workflow.property_address,

        current_stage=workflow.current_stage.value,

        offer_amount=workflow.offer_amount,

        notes=workflow.notes,

    )
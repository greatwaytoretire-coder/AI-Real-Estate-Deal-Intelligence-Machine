from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.api.schemas.pipeline import (
    AcquisitionPipelineRequest,
    AcquisitionPipelineResponse,
)

from ai_real_estate_deal_intelligence_machine.pipelines.acquisition_pipeline import (
    AcquisitionPipeline,
)


router = APIRouter(
    prefix="/pipelines",
    tags=["pipelines"],
)


@router.post(
    "/acquisition",
    response_model=AcquisitionPipelineResponse,
)
def run_acquisition_pipeline(
    request: AcquisitionPipelineRequest,
):

    pipeline = AcquisitionPipeline()

    result = pipeline.execute(
        property_id=request.property_id,
        purchase_price=request.purchase_price,
        estimated_value=request.estimated_value,
        repair_cost=request.repair_cost,
    )

    return AcquisitionPipelineResponse(
        property_id=result.property_id,
        qualified=result.qualified,
        deal_score=result.deal_score,
        recommendation=result.recommendation,
        status=result.status,
    )
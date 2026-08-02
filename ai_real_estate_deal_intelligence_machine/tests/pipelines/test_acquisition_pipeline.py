from ai_real_estate_deal_intelligence_machine.pipelines.acquisition_pipeline import (
    AcquisitionPipeline,
)


def test_acquisition_pipeline_execution():

    pipeline = AcquisitionPipeline()

    result = pipeline.execute(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )

    assert result.property_id == "PROP-001"
    assert result.status == "COMPLETED"
    assert result.recommendation is not None
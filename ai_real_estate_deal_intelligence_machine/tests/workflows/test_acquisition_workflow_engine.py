from ai_real_estate_deal_intelligence_machine.workflows.acquisition.acquisition_workflow_engine import (
    AcquisitionWorkflowEngine,
    AcquisitionStage,
)



def test_acquisition_workflow_advancement():

    engine = AcquisitionWorkflowEngine()


    workflow = engine.advance_stage(
        seller_id="SELLER-001",
        new_stage=AcquisitionStage.CONTACT_ATTEMPTED,
        note="Initial seller contact completed.",
    )


    assert workflow.seller_id == "SELLER-001"

    assert (
        workflow.current_stage
        ==
        AcquisitionStage.CONTACT_ATTEMPTED
    )


    assert (
        "Initial seller contact completed."
        in workflow.notes
    )
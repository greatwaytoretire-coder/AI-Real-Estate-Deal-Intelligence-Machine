from ai_real_estate_deal_intelligence_machine.workflows.deal_intelligence_workflow import (
    DealIntelligenceWorkflow,
)


def test_deal_intelligence_workflow():

    workflow = DealIntelligenceWorkflow()

    result = workflow.execute(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )


    assert result.analysis.property_id == "PROP-001"

    assert result.analysis.projected_profit == 65000

    assert result.report.property_id == "PROP-001"

    assert result.recommendation.property_id == "PROP-001"


def test_deal_intelligence_workflow_recommendation():

    workflow = DealIntelligenceWorkflow()

    result = workflow.execute(
        property_id="PROP-002",
        purchase_price=220000,
        estimated_value=230000,
        repair_cost=20000,
    )


    assert result.analysis.projected_profit == -10000

    assert result.report.property_id == "PROP-002"

    assert result.recommendation.recommendation in [
        "NEGOTIATE",
        "PASS",
    ]
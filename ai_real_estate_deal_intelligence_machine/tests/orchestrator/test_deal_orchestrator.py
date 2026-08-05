from ai_real_estate_deal_intelligence_machine.orchestrator.deal_orchestrator import (
    DealOrchestrator,
)


def test_deal_orchestrator_completes_workflow():

    orchestrator = DealOrchestrator()

    result = orchestrator.execute(
        deal_id="DEAL-001"
    )

    assert result.status == "COMPLETED"

    assert len(result.completed_steps) > 0

    assert "underwriting" in result.completed_steps
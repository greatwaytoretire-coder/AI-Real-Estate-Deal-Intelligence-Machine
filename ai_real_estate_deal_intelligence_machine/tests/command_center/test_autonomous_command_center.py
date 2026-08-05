from ai_real_estate_deal_intelligence_machine.command_center.command_center_models import (
    DealCommandRequest,
)

from ai_real_estate_deal_intelligence_machine.command_center.autonomous_command_center import (
    AutonomousCommandCenter,
)


def test_autonomous_command_center_executes_deal():

    center = AutonomousCommandCenter()

    request = DealCommandRequest(
        deal_id="DEAL100",
        property_address="100 Main Street",
        requested_action="analyze",
    )

    result = center.execute(request)

    assert result.status == "completed"
    assert result.deal_id == "DEAL100"
    assert len(result.actions) == 4
from ai_real_estate_deal_intelligence_machine.agent_bus.integration_bus import (
    AgentIntegrationBus,
)

from ai_real_estate_deal_intelligence_machine.workflow.autonomous_workflow_engine import (
    AutonomousWorkflowEngine,
)


def test_autonomous_workflow_executes_multiple_agents():

    bus = AgentIntegrationBus()

    agents = [
        "acquisition",
        "underwriting",
        "buyer_matching",
        "packaging",
        "execution",
    ]

    for agent in agents:

        bus.register_agent(
            agent,
            lambda payload: {
                "completed": True
            },
        )

    engine = AutonomousWorkflowEngine(bus)

    result = engine.execute(
        "DEAL-1001"
    )

    assert result.status == "COMPLETED"

    assert len(result.completed_agents) == 5

    assert "underwriting" in result.completed_agents
from ai_real_estate_deal_intelligence_machine.agent_bus.integration_bus import (
    AgentIntegrationBus,
)

from ai_real_estate_deal_intelligence_machine.agent_bus.agent_bus_models import (
    AgentRequest,
)

from .workflow_models import WorkflowExecutionResult


class AutonomousWorkflowEngine:

    def __init__(
        self,
        bus: AgentIntegrationBus,
    ):
        self.bus = bus

    def execute(
        self,
        deal_id: str,
    ):

        agents = [
            "acquisition",
            "underwriting",
            "buyer_matching",
            "packaging",
            "execution",
        ]

        completed_agents = []

        for agent in agents:

            response = self.bus.execute(
                AgentRequest(
                    agent_name=agent,
                    action="process",
                    payload={
                        "deal_id": deal_id
                    },
                )
            )

            if response.success:
                completed_agents.append(agent)

        return WorkflowExecutionResult(
            deal_id=deal_id,
            completed_agents=completed_agents,
            status="COMPLETED",
            message="Autonomous multi-agent workflow completed.",
        )
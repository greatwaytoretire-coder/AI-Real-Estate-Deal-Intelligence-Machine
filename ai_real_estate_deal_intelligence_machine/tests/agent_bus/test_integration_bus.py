from ai_real_estate_deal_intelligence_machine.agent_bus.integration_bus import (
    AgentIntegrationBus,
)

from ai_real_estate_deal_intelligence_machine.agent_bus.agent_bus_models import (
    AgentRequest,
)


def test_agent_integration_bus_executes_registered_agent():

    bus = AgentIntegrationBus()

    def mock_underwriting(payload):
        return {
            "decision": "BUY",
            "score": 90,
        }

    bus.register_agent(
        "underwriting",
        mock_underwriting,
    )

    response = bus.execute(
        AgentRequest(
            agent_name="underwriting",
            action="analyze",
            payload={
                "price": 250000
            },
        )
    )

    assert response.success is True

    assert response.result["decision"] == "BUY"

    assert response.agent_name == "underwriting"
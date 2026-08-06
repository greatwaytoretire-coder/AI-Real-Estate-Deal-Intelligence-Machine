from ai_real_estate_deal_intelligence_machine.agent_bus.integration_bus import (
    AgentIntegrationBus,
)

from ai_real_estate_deal_intelligence_machine.workflow.autonomous_workflow_engine import (
    AutonomousWorkflowEngine,
)

from ai_real_estate_deal_intelligence_machine.orchestrator.deal_orchestrator import (
    DealOrchestrator,
)

from ai_real_estate_deal_intelligence_machine.command_center.autonomous_command_center import (
    AutonomousCommandCenter,
)

from ai_real_estate_deal_intelligence_machine.dashboard.deal_dashboard import (
    DealDashboard,
)

from ai_real_estate_deal_intelligence_machine.application_service import (
    ApplicationService,
)


def register_agents(bus):

    """
    Register autonomous agents
    into the application runtime.
    """

    bus.register_agent(
        "acquisition",
        lambda payload: {
            "agent": "acquisition",
            "result": "Seller acquisition analysis complete",
            "payload": payload,
        },
    )


    bus.register_agent(
        "underwriting",
        lambda payload: {
            "agent": "underwriting",
            "result": "Deal underwriting complete",
            "payload": payload,
        },
    )


    bus.register_agent(
        "buyer_matching",
        lambda payload: {
            "agent": "buyer_matching",
            "result": "Buyer matching complete",
            "payload": payload,
        },
    )


    bus.register_agent(
        "packaging",
        lambda payload: {
            "agent": "packaging",
            "result": "Deal package generated",
            "payload": payload,
        },
    )


    bus.register_agent(
        "execution",
        lambda payload: {
            "agent": "execution",
            "result": "Execution workflow complete",
            "payload": payload,
        },
    )



def build_application():

    bus = AgentIntegrationBus()


    #
    # Register autonomous agent network
    #

    register_agents(bus)


    workflow_engine = AutonomousWorkflowEngine(
        bus=bus
    )


    orchestrator = DealOrchestrator()


    command_center = AutonomousCommandCenter()


    dashboard = DealDashboard()



    service = ApplicationService(
        command_center=command_center,
        workflow_engine=workflow_engine,
        orchestrator=orchestrator,
        dashboard=dashboard,
        bus=bus,
    )


    return service



def main():

    print("=" * 70)
    print("AI REAL ESTATE DEAL INTELLIGENCE MACHINE")
    print("AUTONOMOUS APPLICATION ONLINE")
    print("=" * 70)


    application = build_application()


    result = application.analyze_deal(
        deal_id="DEAL-001"
    )


    print()

    print("=" * 70)
    print("FINAL SYSTEM RESULT")
    print("=" * 70)

    print(result)



if __name__ == "__main__":
    main()
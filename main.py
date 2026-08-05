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


def build_application():

    bus = AgentIntegrationBus()

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
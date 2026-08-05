from datetime import datetime, timezone


class ApplicationService:
    """
    Main runtime coordinator.

    Connects:
    - Command Center
    - Workflow Engine
    - Orchestrator
    - Dashboard
    - Agent Runtime
    """

    def __init__(
        self,
        command_center,
        workflow_engine,
        orchestrator,
        dashboard,
        bus,
    ):

        self.command_center = command_center
        self.workflow_engine = workflow_engine
        self.orchestrator = orchestrator
        self.dashboard = dashboard
        self.bus = bus

        self.register_core_agents()


    def register_core_agents(self):
        """
        Register the first operational AI agents.
        """

        self.bus.register_agent(
            "acquisition",
            self.acquisition_agent,
        )

        self.bus.register_agent(
            "underwriting",
            self.underwriting_agent,
        )

        self.bus.register_agent(
            "buyer_matching",
            self.buyer_matching_agent,
        )

        self.bus.register_agent(
            "packaging",
            self.packaging_agent,
        )

        self.bus.register_agent(
            "execution",
            self.execution_agent,
        )


    def acquisition_agent(self, payload):
        return {
            "stage": "acquisition",
            "deal_id": payload["deal_id"],
            "status": "analyzed",
        }


    def underwriting_agent(self, payload):
        return {
            "stage": "underwriting",
            "deal_id": payload["deal_id"],
            "status": "underwritten",
        }


    def buyer_matching_agent(self, payload):
        return {
            "stage": "buyer_matching",
            "deal_id": payload["deal_id"],
            "status": "buyers_matched",
        }


    def packaging_agent(self, payload):
        return {
            "stage": "packaging",
            "deal_id": payload["deal_id"],
            "status": "package_created",
        }


    def execution_agent(self, payload):
        return {
            "stage": "execution",
            "deal_id": payload["deal_id"],
            "status": "ready",
        }


    def analyze_deal(
        self,
        deal_id: str,
    ):

        print()
        print("=" * 70)
        print("AUTONOMOUS DEAL ANALYSIS STARTED")
        print("=" * 70)

        print(f"Deal ID: {deal_id}")


        workflow_result = self.workflow_engine.execute(
            deal_id
        )


        if hasattr(self.dashboard, "record_activity"):

            self.dashboard.record_activity(
                deal_id=deal_id,
                activity="Autonomous deal analysis completed",
            )


        print()
        print("DEAL ANALYSIS COMPLETE")
        print()

        print(workflow_result)


        return {
            "deal_id": deal_id,
            "started_at": datetime.now(timezone.utc),
            "status": "COMPLETED",
            "workflow": workflow_result,
        }
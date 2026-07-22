import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase30 import ContinuousRuntime, OperatingMode
from ai_real_estate_deal_intelligence_machine.phase36 import (
    AgentOrchestrator,
    AgentWorkflow,
)
from ai_real_estate_deal_intelligence_machine.phase8 import DealRiskAgent
from ai_real_estate_deal_intelligence_machine.phase5 import OpportunityScoringEngine


class Phase36WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("data/test_phase36_workflow.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)

    def test_end_to_end_agent_workflow(self):
        """
        PHASE 36: Verify that the orchestrator can execute a multi-step agent workflow.
        """
        # 1. Initialize all necessary components
        provider_manager = ProviderManager(audit_logger=self.audit_logger)
        orchestrator = AgentOrchestrator(audit_logger=self.audit_logger)
        runtime = ContinuousRuntime(self.audit_logger, provider_manager, orchestrator)
        runtime.mode = OperatingMode.PILOT

        # 2. Define and register a workflow
        discovery_workflow = AgentWorkflow(
            name="Standard Property Analysis",
            steps=[
                DealRiskAgent(self.audit_logger),
                OpportunityScoringEngine(self.audit_logger),
            ],
        )
        orchestrator.register_workflow("PROPERTY_DISCOVERED", discovery_workflow)

        # 3. Run ingestion to create a job with the 'PROPERTY_DISCOVERED' event type
        runtime.run_ingestion("attom", {"zip": "12345"})
        self.assertEqual(len(runtime.job_queue.pending_queue), 1)

        # 4. Run the worker to process the job
        runtime.worker.run()

        # 5. Verify the logs to ensure the workflow executed correctly
        with self.log_path.open("r") as f:
            log_contents = f.read()
            self.assertIn("Starting workflow 'Standard Property Analysis'", log_contents)
            self.assertIn("AGENT_EXECUTE_START: DealRiskAgent", log_contents)
            self.assertIn("AGENT_EXECUTE_START: OpportunityScoringEngine", log_contents)
            self.assertIn("Orchestrator workflow 'Standard Property Analysis' completed", log_contents)
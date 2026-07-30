import unittest
import unittest.mock
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase30 import ContinuousRuntime, OperatingMode
from ai_real_estate_deal_intelligence_machine.phase36 import (
    AgentOrchestrator,
    AgentWorkflow,
)
from ai_real_estate_deal_intelligence_machine.phase29 import ScalingManager
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase5 import ScoringInput
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
        orchestrator = AgentOrchestrator(audit_logger=self.audit_logger)
        risk_agent = DealRiskAgent(self.audit_logger)
        scoring_agent = OpportunityScoringEngine(self.audit_logger)

        # 2. Define and register a workflow
        discovery_workflow = AgentWorkflow(
            name="Standard Property Analysis",
            steps=[risk_agent, scoring_agent],
            input_factories={
                "DealRiskAgent": lambda j: unittest.mock.MagicMock(),
                "OpportunityScoringEngine": lambda j: ScoringInput(correlation_id=j.job_id),
            },
        )
        orchestrator.register_workflow("PROPERTY_DISCOVERED", discovery_workflow)

        # Mock the runtime environment
        provider_manager = ProviderManager(audit_logger=self.audit_logger)
        provider_manager.providers = {"mock_market": unittest.mock.MagicMock()}
        provider_manager.providers["mock_market"].fetch.return_value = [
            {"id": "rec-001", "provider": "mock_market", "address": "123 Main St", "zip": "12345"}
        ]
        scaling_manager = ScalingManager()
        scaling_manager.load_market_config(unittest.mock.MagicMock(market_id="test_market", status="ACTIVE", data_providers=["mock_market"]))

        runtime = ContinuousRuntime(
            self.audit_logger, provider_manager, orchestrator, scaling_manager=scaling_manager
        )
        runtime.mode = OperatingMode.PILOT

        # 3. Run ingestion to create a job with the 'PROPERTY_DISCOVERED' event type
        runtime.run_ingestion_for_market("test_market", {})
        # The in-memory queue is a list of IDs
        self.assertEqual(len(runtime.job_queue.pending_queue), 1) # type: ignore

        # 4. Run the worker to process the job
        runtime.worker.run()

        # 5. Verify the logs to ensure the workflow executed correctly
        with self.log_path.open("r") as f:
            log_contents = f.read()
            self.assertIn("ORCHESTRATOR_WORKFLOW_START", log_contents)
            self.assertIn("DealRiskAgent starting", log_contents)
            self.assertIn("OpportunityScoringEngine starting", log_contents)
            self.assertIn("ORCHESTRATOR_WORKFLOW_SUCCESS", log_contents)
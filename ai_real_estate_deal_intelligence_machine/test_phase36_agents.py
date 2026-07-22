import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase8 import (
    DealRiskAgent,
    DealRiskAgentInput,
    DealRiskAgentOutput,
)
from ai_real_estate_deal_intelligence_machine.phase30 import Job
from ai_real_estate_deal_intelligence_machine.phase36 import AgentContract, AgentOrchestrator


class Phase36AgentContractTest(unittest.TestCase):
    def setUp(self):
        log_path = Path("data/test_phase36_audit.log")
        log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=log_path)

    def test_deal_risk_agent_implements_contract(self):
        """
        PHASE 36: Verify that an agent correctly implements the standard contract.
        """
        agent = DealRiskAgent(audit_logger=self.audit_logger)

        # 1. Verify the contract definition
        contract = agent.get_contract()
        self.assertIsInstance(contract, AgentContract)
        self.assertEqual(contract.agent_name, "DealRiskAgent")
        self.assertEqual(contract.version, "2.0.0")

        # 2. Verify execution with standard inputs and outputs
        agent_input = DealRiskAgentInput(correlation_id="corr-123", deal_id="deal-abc")
        agent_output = agent.execute(agent_input)

        self.assertIsInstance(agent_output, DealRiskAgentOutput)
        self.assertIsNone(agent_output.error)
        self.assertGreater(agent_output.confidence, 0.8)
        self.assertIsNotNone(agent_output.assessment)
        self.assertEqual(agent_output.assessment.risk_score, 72)

    def test_agent_orchestrator_routes_job(self):
        """
        PHASE 36: Verify the orchestrator routes a job to the correct agent.
        """
        orchestrator = AgentOrchestrator(audit_logger=self.audit_logger)
        risk_agent = DealRiskAgent(audit_logger=self.audit_logger)

        # Register the agent to handle a specific event type
        orchestrator.register_agent("PROPERTY_DISCOVERED", risk_agent)

        # Create a job that should be handled by the risk agent
        job = Job(job_id="job-risk-01", payload={"event_type": "PROPERTY_DISCOVERED", "deal_id": "deal-abc"})
        output = orchestrator.handle_job(job)

        self.assertIsInstance(output, DealRiskAgentOutput)
        self.assertIsNone(output.error)
        self.assertEqual(output.assessment.risk_score, 72)

        # Create a job with an unregistered event type
        bad_job = Job(job_id="job-bad-01", payload={"event_type": "UNKNOWN_EVENT"})
        bad_output = orchestrator.handle_job(bad_job)
        self.assertIsNotNone(bad_output.error)
        self.assertIn("No agent registered", bad_output.error)
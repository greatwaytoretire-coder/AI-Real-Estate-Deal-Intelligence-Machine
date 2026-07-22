import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase25 import (
    ApprovalStatus,
    HumanInTheLoopEngine,
)
from ai_real_estate_deal_intelligence_machine.phase33 import (
    AIPrediction,
    ActualOutcome,
    ValidationManager,
)
from ai_real_estate_deal_intelligence_machine.phase38 import LearningPipelineOrchestrator


class Phase38LearningPipelineTest(unittest.TestCase):
    def setUp(self):
        log_path = Path("data/test_phase38_audit.log")
        log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=log_path)
        self.validation_manager = ValidationManager()
        self.hitl_engine = HumanInTheLoopEngine(audit_logger=self.audit_logger)
        self.orchestrator = LearningPipelineOrchestrator(self.validation_manager, self.hitl_engine)

    def test_learning_pipeline_creates_approval_action(self):
        """
        PHASE 38: Verify the learning pipeline creates a proposal for human approval.
        """
        deal_id = "deal-learn-01"

        # Create a prediction and an outcome with a significant error
        prediction = AIPrediction(deal_id=deal_id, estimated_arv=300000)
        outcome = ActualOutcome(deal_id=deal_id, actual_sale_price=250000)
        self.validation_manager.record_prediction(prediction)
        self.validation_manager.record_outcome(outcome)

        # Run the learning pipeline for this deal
        proposal = self.orchestrator.run_for_deal(deal_id)

        # Verify that a proposal was generated and submitted for approval
        self.assertIsNotNone(proposal)
        self.assertEqual(len(self.hitl_engine.approval_queue), 1)

        action = self.hitl_engine.approval_queue[0]
        self.assertEqual(action.status, ApprovalStatus.PENDING_REVIEW)
        self.assertEqual(action.action_type, "MODEL_UPDATE_PROPOSAL")
        self.assertIn("ARV was Overestimated by 20.00%", action.reasoning)
        self.assertEqual(action.action_payload["target_model"], "ARV_ESTIMATION")
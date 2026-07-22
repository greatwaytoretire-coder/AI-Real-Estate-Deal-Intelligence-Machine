import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase25 import (
    ActionForApproval,
    ApprovalStatus,
    HumanInTheLoopEngine,
    PendingActionDashboard,
)


class Phase25HumanInTheLoopTest(unittest.TestCase):
    def setUp(self):
        """Set up a fresh engine and logger for each test."""
        self.log_path = Path("data/test_phase25_audit.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)
        self.hitl_engine = HumanInTheLoopEngine(audit_logger=self.audit_logger)

    def tearDown(self):
        """Clean up log files after tests."""
        self.log_path.unlink(missing_ok=True)

    def test_human_in_the_loop_workflow(self):
        """
        PHASE 25: Verify the complete human-in-the-loop approval workflow.
        """
        # 1. An AI agent generates an action that requires approval.
        action = ActionForApproval(
            action_type="SELLER_OUTREACH",
            recommendation="Send initial outreach email to seller of 123 Main St.",
            reasoning="Property meets high-equity and vacant signals. Seller is a strong candidate.",
            supporting_data={"property_address": "123 Main St", "seller_id": "seller-abc"},
            confidence_score=0.92,
            risk_assessment={"level": "LOW", "notes": "No known risks."},
            action_payload={"to": "seller@example.com", "subject": "Regarding your property at 123 Main St"},
        )

        # 2. The action is submitted to the HITL engine.
        self.hitl_engine.submit_for_approval(action)
        self.assertEqual(action.status, ApprovalStatus.PENDING_REVIEW)
        self.assertEqual(len(self.hitl_engine.approval_queue), 1)

        # 3. The pending action dashboard should show the action.
        dashboard = PendingActionDashboard(self.hitl_engine)
        report = dashboard.generate_report()
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0]["action_id"], action.action_id)

        # 4. A human operator approves the action.
        operator_id = "gregory_human_operator"
        approved = self.hitl_engine.approve(action.action_id, operator_id=operator_id)
        self.assertTrue(approved)
        self.assertEqual(action.status, ApprovalStatus.APPROVED)

        # 5. Verify the audit trail.
        self.assertEqual(len(action.audit_history), 3)
        self.assertEqual(action.audit_history[-1].status, ApprovalStatus.APPROVED)
        self.assertEqual(action.audit_history[-1].operator_id, operator_id)

        # Verify the persistent audit log contains the approval record.
        with self.log_path.open("r") as f:
            log_contents = f.read()
            self.assertIn(f"Action {action.action_id} approved by {operator_id}", log_contents)

        # 6. Test rejection
        action2 = ActionForApproval(action_type="BUYER_OUTREACH")
        self.hitl_engine.submit_for_approval(action2)
        rejected = self.hitl_engine.reject(action2.action_id, operator_id, "Not a good fit.")
        self.assertTrue(rejected)
        self.assertEqual(action2.status, ApprovalStatus.REJECTED)
        self.assertEqual(action2.audit_history[-1].status, ApprovalStatus.REJECTED)

        # 7. Test edit
        action3 = ActionForApproval(action_type="DEAL_PACKAGE_DISTRIBUTION")
        self.hitl_engine.submit_for_approval(action3)
        edited = self.hitl_engine.edit(action3.action_id, operator_id, {"new": "payload"})
        self.assertTrue(edited)
        self.assertEqual(action3.status, ApprovalStatus.PENDING_REVIEW) # Status reverts to pending
        self.assertEqual(action3.action_payload, {"new": "payload"})
        # Audit history should now have 4 entries: DRAFT -> PENDING -> DRAFT -> PENDING
        self.assertEqual(len(action3.audit_history), 4)
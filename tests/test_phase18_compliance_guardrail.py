import unittest

from ai_real_estate_deal_intelligence_machine.phase18 import (
    ComplianceAuditTrail,
    ComplianceGuardrailAgent,
    GuardrailDecision,
)


class Phase18ComplianceGuardrailTests(unittest.TestCase):
    def test_guardrail_decision_and_audit_trail_are_created(self):
        decision = GuardrailDecision(
            agent="ComplianceGuardrailAgent",
            trigger="unauthorized data access",
            input_data={"source": "test"},
            decision="block",
            action="escalate",
            result="blocked",
        )
        audit = ComplianceAuditTrail(
            agent="ComplianceGuardrailAgent",
            trigger="unauthorized data access",
            input_data={"source": "test"},
            decision="block",
            action="escalate",
            result="blocked",
        )

        self.assertEqual(decision.decision, "block")
        self.assertEqual(audit.action, "escalate")

    def test_compliance_guardrail_agent_blocks_unsafe_actions(self):
        agent = ComplianceGuardrailAgent()
        result = agent.evaluate_action(
            agent_name="BuyerDispositionAgent",
            trigger="excessive outreach",
            input_data={"contacts": 100},
            decision="block",
            action="escalate",
            result="blocked",
        )

        self.assertTrue(result["allowed"] is False)
        self.assertEqual(result["decision"], "block")


if __name__ == "__main__":
    unittest.main()

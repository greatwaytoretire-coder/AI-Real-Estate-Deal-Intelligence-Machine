import unittest

from ai_real_estate_deal_intelligence_machine.phase8 import (
    DealRiskAgent,
    RiskAssessment,
)


class Phase8RiskEngineTests(unittest.TestCase):
    def test_risk_assessment_has_required_fields(self):
        assessment = RiskAssessment(
            risk_score=72,
            critical_risk=True,
            warning="Insufficient spread",
            information_gap="Buyer demand snapshot missing",
        )

        self.assertGreaterEqual(assessment.risk_score, 0)
        self.assertTrue(assessment.critical_risk)
        self.assertIn("warning", assessment.as_dict())
        self.assertIn("information_gap", assessment.as_dict())

    def test_deal_risk_agent_blocks_promotion_on_critical_risk(self):
        agent = DealRiskAgent()
        blocked = agent.evaluate_risk()

        self.assertTrue(blocked["auto_promotion_blocked"])
        self.assertTrue(blocked["critical_risk"])


if __name__ == "__main__":
    unittest.main()

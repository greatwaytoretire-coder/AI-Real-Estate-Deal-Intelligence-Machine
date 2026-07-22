import unittest

from ai_real_estate_deal_intelligence_machine.phase11 import (
    SellerAcquisitionAgent,
    SellerOpportunity,
    SellerQualificationPlan,
    SellerStage,
)


class Phase11SellerAcquisitionTests(unittest.TestCase):
    def test_seller_stage_enum_has_required_stages(self):
        self.assertIn(SellerStage.DISCOVERED, SellerStage)
        self.assertIn(SellerStage.RESEARCHING, SellerStage)
        self.assertIn(SellerStage.CONTACTING, SellerStage)
        self.assertIn(SellerStage.ENGAGED, SellerStage)
        self.assertIn(SellerStage.QUALIFIED, SellerStage)
        self.assertIn(SellerStage.NEGOTIATING, SellerStage)
        self.assertIn(SellerStage.OFFER, SellerStage)
        self.assertIn(SellerStage.CONTRACT, SellerStage)
        self.assertIn(SellerStage.CLOSED, SellerStage)
        self.assertIn(SellerStage.LOST, SellerStage)

    def test_seller_acquisition_agent_builds_qualification_and_outreach(self):
        agent = SellerAcquisitionAgent()
        opportunity = agent.identify_high_priority_opportunity()
        qualification = agent.build_qualification_plan(opportunity)
        outreach = agent.generate_outreach(opportunity)

        self.assertIsInstance(opportunity, SellerOpportunity)
        self.assertIsInstance(qualification, SellerQualificationPlan)
        self.assertTrue(outreach)

    def test_opt_out_and_preferences_are_respected(self):
        agent = SellerAcquisitionAgent()
        andy = agent.identify_high_priority_opportunity()
        self.assertFalse(andy.opt_out)
        self.assertEqual(andy.communication_preference, "email")


if __name__ == "__main__":
    unittest.main()

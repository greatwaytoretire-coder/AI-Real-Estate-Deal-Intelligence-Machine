import unittest

from ai_real_estate_deal_intelligence_machine.phase12 import (
    BuyerDispositionAgent,
    BuyerInterestClassification,
    BuyerDispositionSummary,
)


class Phase12BuyerDispositionTests(unittest.TestCase):
    def test_classifications_include_required_states(self):
        self.assertIn(BuyerInterestClassification.INTERESTED, BuyerInterestClassification)
        self.assertIn(BuyerInterestClassification.WANTS_DETAILS, BuyerInterestClassification)
        self.assertIn(BuyerInterestClassification.WANTS_A_CALL, BuyerInterestClassification)
        self.assertIn(BuyerInterestClassification.WANTS_TO_SUBMIT_OFFER, BuyerInterestClassification)
        self.assertIn(BuyerInterestClassification.NOT_INTERESTED, BuyerInterestClassification)
        self.assertIn(BuyerInterestClassification.DO_NOT_CONTACT, BuyerInterestClassification)

    def test_disposition_agent_generates_summary_outreach_and_follow_up(self):
        agent = BuyerDispositionAgent()
        summary = agent.generate_deal_summary()
        buyers = agent.identify_buyers()
        outreach = agent.create_outreach(buyers[0])
        follow_up = agent.create_follow_up_workflow(buyers[0])

        self.assertIsInstance(summary, BuyerDispositionSummary)
        self.assertTrue(buyers)
        self.assertTrue(outreach)
        self.assertTrue(follow_up)

    def test_disposition_agent_classifies_interest(self):
        agent = BuyerDispositionAgent()
        classification = agent.classify_buyer_interest()
        self.assertIn(classification, BuyerInterestClassification)


if __name__ == "__main__":
    unittest.main()

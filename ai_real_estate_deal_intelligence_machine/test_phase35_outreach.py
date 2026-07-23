import unittest

from ai_real_estate_deal_intelligence_machine.phase11 import SellerOpportunity, SellerStage
from ai_real_estate_deal_intelligence_machine.phase34 import DealContext, EnhancedBuyerProfile
from ai_real_estate_deal_intelligence_machine.phase35 import CommunicationContentAgent


class Phase35OutreachTest(unittest.TestCase):
    def setUp(self):
        self.agent = CommunicationContentAgent()
        self.deal = DealContext(
            deal_id="deal-outreach-01",
            zip_code="78704",
            property_type="Single Family",
            purchase_price=350000,
            estimated_rehab_level="moderate",
            investment_strategy="Fix and Flip",
        )

    def test_generate_buyer_outreach_draft(self):
        """
        PHASE 35: Verify buyer outreach draft generation.
        """
        buyer = EnhancedBuyerProfile(name="Jane Investor")
        draft = self.agent.generate_buyer_outreach_draft(self.deal, buyer)

        self.assertEqual(draft.recipient_type, "buyer")
        self.assertIn("78704", draft.subject)
        self.assertIn("Hello Jane Investor", draft.body)
        self.assertIn("estimated purchase price", draft.body)
        self.assertIn("opt-out", draft.body)
        self.assertNotIn("guarantee", draft.body.lower())

    def test_generate_seller_outreach_draft(self):
        """
        PHASE 35: Verify seller outreach draft generation.
        """
        seller = SellerOpportunity(
            seller_id="seller-outreach-01",
            stage=SellerStage.DISCOVERED,
            priority="HIGH",
            signal_summary="",
            missing_information=[],
            opt_out=False,
            communication_preference="email",
        )
        draft = self.agent.generate_seller_outreach_draft(self.deal, seller)

        self.assertEqual(draft.recipient_type, "seller")
        self.assertIn(self.deal.zip_code, draft.subject)
        self.assertIn("no-obligation offer", draft.body)
        self.assertIn("opt-out", draft.body)
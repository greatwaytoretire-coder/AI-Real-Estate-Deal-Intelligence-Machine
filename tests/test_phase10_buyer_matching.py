import unittest

from ai_real_estate_deal_intelligence_machine.phase10 import (
    BuyerMatchOpportunity,
    BuyerMatchingEngine,
    BuyerRankedMatch,
)


class Phase10BuyerMatchingTests(unittest.TestCase):
    def test_buyer_matching_engine_ranks_matches(self):
        engine = BuyerMatchingEngine()
        opportunities = engine.gather_opportunities()

        self.assertEqual(opportunities[0].buyer_id, "buyer-0001")
        self.assertGreaterEqual(opportunities[0].score, 0)
        self.assertEqual(opportunities[0].category, "TOP 10 BUYER MATCHES")

    def test_ranked_buyer_matches_include_top_lists(self):
        engine = BuyerMatchingEngine()
        ranked = engine.rank_buyers()

        self.assertIn("TOP 10 BUYER MATCHES", ranked)
        self.assertIn("TOP VERIFIED BUYERS", ranked)
        self.assertIn("TOP HIGH-RELIABILITY BUYERS", ranked)
        self.assertIn("TOP RECENTLY ACTIVE BUYERS", ranked)

    def test_outreach_opportunities_are_created(self):
        engine = BuyerMatchingEngine()
        outreach = engine.create_outreach_opportunities()

        self.assertTrue(outreach)
        self.assertIn("buyer-0001", outreach[0]["buyer_id"])


if __name__ == "__main__":
    unittest.main()

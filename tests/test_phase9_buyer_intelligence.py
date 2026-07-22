import unittest

from ai_real_estate_deal_intelligence_machine.phase9 import (
    BuyerActivityProfile,
    BuyerIntelligenceEngine,
    BuyerMatchScore,
    BuyerProfile,
    BuyerReliabilityScore,
)


class Phase9BuyerIntelligenceTests(unittest.TestCase):
    def test_buyer_profile_tracks_required_dimensions(self):
        profile = BuyerProfile(
            buyer_id="buyer-0001",
            geography="Austin, TX",
            purchase_range=(150000, 260000),
            property_type="single-family",
            strategy="fix-and-flip",
            proof_of_funds="bank statement snapshot",
            verification_status="VERIFIED",
        )

        self.assertEqual(profile.geography, "Austin, TX")
        self.assertEqual(profile.property_type, "single-family")
        self.assertEqual(profile.strategy, "fix-and-flip")
        self.assertTrue(profile.verified)

    def test_buyer_intelligence_engine_creates_profiles_scores_and_event(self):
        agent = BuyerIntelligenceEngine()
        activity = agent.build_activity_profile()
        match_score = agent.score_match()
        reliability = agent.score_reliability()
        event = agent.generate_event()

        self.assertIsInstance(activity, BuyerActivityProfile)
        self.assertIsInstance(match_score, BuyerMatchScore)
        self.assertIsInstance(reliability, BuyerReliabilityScore)
        self.assertEqual(event.event_type, "BUYER_INTELLIGENCE_UPDATED")
        self.assertIn("buyer", event.payload)
        self.assertIn("activity", event.payload)
        self.assertIn("match_score", event.payload)
        self.assertIn("reliability", event.payload)

    def test_unverified_buyer_is_not_marked_verified_without_evidence(self):
        profile = BuyerProfile(
            buyer_id="buyer-0002",
            geography="Dallas, TX",
            purchase_range=(200000, 350000),
            property_type="multi-family",
            strategy="buy-and-hold",
            proof_of_funds=None,
            verification_status="UNVERIFIED",
        )

        self.assertFalse(profile.verified)


if __name__ == "__main__":
    unittest.main()

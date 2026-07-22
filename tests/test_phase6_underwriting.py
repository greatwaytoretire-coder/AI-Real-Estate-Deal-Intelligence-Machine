import unittest

from ai_real_estate_deal_intelligence_machine.phase6 import (
    ARVEstimate,
    ComparableSalesAgent,
    RepairEstimate,
    RepairItem,
)


class Phase6UnderwritingTests(unittest.TestCase):
    def test_comparable_sales_agent_can_rank_comps(self):
        agent = ComparableSalesAgent()
        comps = agent.identify_comparables()

        self.assertGreaterEqual(len(comps), 1)
        self.assertTrue(all("comparable" in comp for comp in comps))

    def test_arv_estimate_contains_confidence_and_range(self):
        estimate = ARVEstimate(low=180000, high=195000, confidence=0.85, source="mock")
        self.assertLess(estimate.low, estimate.high)
        self.assertGreaterEqual(estimate.confidence, 0)
        self.assertEqual(estimate.source, "mock")

    def test_repair_estimate_tracks_components_and_assumptions(self):
        repair = RepairEstimate(
            low=10000,
            high=15000,
            confidence=0.78,
            source="mock",
            assumptions=["roof", "hvac", "plumbing"],
            repairs=[RepairItem(category="roof", low=3000, high=5000)],
        )

        self.assertTrue(repair.assumptions)
        self.assertGreaterEqual(len(repair.repairs), 1)


if __name__ == "__main__":
    unittest.main()

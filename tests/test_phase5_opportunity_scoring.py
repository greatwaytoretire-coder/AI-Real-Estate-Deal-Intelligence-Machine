import unittest

from ai_real_estate_deal_intelligence_machine.phase5 import (
    DealScorecard,
    OpportunityScoringEngine,
    PriorityDealQueue,
)


class Phase5OpportunityScoringTests(unittest.TestCase):
    def test_scorecard_contains_explainable_scores(self):
        scorecard = DealScorecard()

        for key in [
            "opportunity_score",
            "deal_potential_score",
            "market_score",
            "buyer_demand_score",
            "risk_score",
            "data_confidence_score",
            "urgency_score",
        ]:
            self.assertIn(key, scorecard.as_dict())

    def test_engine_promotes_high_scoring_opportunities(self):
        engine = OpportunityScoringEngine()
        queue = PriorityDealQueue()
        promoted = engine.promote_high_scoring(queue)

        self.assertGreaterEqual(len(promoted), 1)
        self.assertTrue(all(item["priority"] >= 0 for item in promoted))


if __name__ == "__main__":
    unittest.main()

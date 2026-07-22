import unittest

from ai_real_estate_deal_intelligence_machine.phase3 import (
    HeatMapEngine,
    MarketIntelligenceAgent,
    MarketScore,
    MarketSnapshot,
)


class Phase3MarketIntelligenceTests(unittest.TestCase):
    def test_market_score_has_required_components(self):
        score = MarketScore()
        self.assertGreaterEqual(score.value, 0)
        self.assertGreaterEqual(score.opportunity_density, 0)
        self.assertGreaterEqual(score.buyer_density, 0)
        self.assertGreaterEqual(score.market_liquidity, 0)

    def test_market_intelligence_agent_can_rank_markets(self):
        agent = MarketIntelligenceAgent()
        rankings = agent.rank_markets()

        self.assertGreaterEqual(len(rankings), 1)
        self.assertTrue(all("market" in row for row in rankings))
        self.assertTrue(all("market_score" in row for row in rankings))

    def test_heat_map_engine_produces_required_map_types(self):
        engine = HeatMapEngine()
        maps = engine.generate_maps()

        for map_name in [
            "opportunity_heat_map",
            "buyer_heat_map",
            "distress_heat_map",
            "investor_activity_heat_map",
            "buyer_opportunity_overlap_map",
        ]:
            self.assertIn(map_name, maps)

    def test_market_snapshot_can_identify_special_market_categories(self):
        snapshot = MarketSnapshot()
        categories = snapshot.classify_market()

        self.assertTrue(any(category in categories for category in [
            "TOP_MARKETS",
            "EMERGING_MARKETS",
            "HIGH-OPPORTUNITY_ZONES",
            "HIGH-BUYER-DEMAND_ZONES",
            "UNDER-SERVED_MARKETS",
        ]))


if __name__ == "__main__":
    unittest.main()

import unittest

from ai_real_estate_deal_intelligence_machine.phase29 import MarketConfig, ScalingManager


class Phase29ScalingArchitectureTest(unittest.TestCase):
    def test_multi_market_configuration_and_controls(self):
        """
        PHASE 29: Verify the scaling manager can handle multiple market configurations
        and enforce budgets and enable/disable flags.
        """
        manager = ScalingManager()

        # 1. Define and load configurations for two markets
        config_austin = MarketConfig(
            market_id="atx",
            market_name="Austin, TX",
            data_providers=["attom_api", "mls_feed_atx"],
            monthly_budget=500.0,
        )
        config_dallas = MarketConfig(
            market_id="dfw",
            market_name="Dallas, TX",
            data_providers=["attom_api", "mls_feed_dfw"],
            is_enabled=False,  # Dallas is initially disabled
        )

        manager.load_market_config(config_austin)
        manager.load_market_config(config_dallas)

        # 2. Verify that only the active market is returned
        active_markets = manager.get_active_markets()
        self.assertEqual(len(active_markets), 1)
        self.assertEqual(active_markets[0].market_id, "atx")

        # 3. Verify budget controls
        self.assertTrue(manager.is_within_budget("atx"))

        # Record usage that exceeds the budget
        manager.record_usage(market_id="atx", api_calls=100, cost=501.0)
        self.assertFalse(manager.is_within_budget("atx"))

        # 4. Enable the second market and verify it becomes active
        dallas_config = manager.get_market_config("dfw")
        self.assertIsNotNone(dallas_config)
        dallas_config.is_enabled = True
        manager.load_market_config(dallas_config)

        active_markets_after_update = manager.get_active_markets()
        self.assertEqual(len(active_markets_after_update), 2)
        market_ids = {m.market_id for m in active_markets_after_update}
        self.assertIn("atx", market_ids)
        self.assertIn("dfw", market_ids)
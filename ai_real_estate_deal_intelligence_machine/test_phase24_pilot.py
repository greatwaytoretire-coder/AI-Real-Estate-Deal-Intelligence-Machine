import unittest

from ai_real_estate_deal_intelligence_machine.phase24 import (
    DataSourceType,
    MarketPilotConfig,
    PilotDashboard,
)


class Phase24PilotFoundationTest(unittest.TestCase):
    def test_run_pilot_dashboard(self):
        """
        PHASE 24: Verify the pilot configuration and dashboard foundation.
        """
        # 1. Create a pilot configuration for a single market
        pilot_config = MarketPilotConfig(
            market_name="Austin, TX",
            state="TX",
            county="Travis",
            target_zip_codes=["78701", "78702", "78704"],
            property_types=["single-family", "duplex"],
            min_price=250000,
            max_price=700000,
            min_equity_percent=0.25,
            max_repair_budget=50000,
            min_deal_score=80.0,
            target_seller_signals=["high-equity", "vacant"],
            target_buyer_criteria={"strategy": "fix-and-flip", "min_transactions": 5},
        )

        self.assertEqual(pilot_config.market_name, "Austin, TX")
        self.assertIn("78704", pilot_config.target_zip_codes)

        # 2. Create and run the pilot dashboard with the configuration
        dashboard = PilotDashboard(config=pilot_config)
        report = dashboard.run_mock_pilot_summary()

        # 3. Verify the report output
        self.assertIsInstance(report, dict)
        self.assertEqual(report["pilot_market"], "Austin, TX")
        self.assertGreater(report["opportunities_discovered"], 0)
        self.assertGreater(len(report["top_ranked_deals"]), 0)
        self.assertIn(DataSourceType.LIVE.value, report["data_sources_in_use"])
        self.assertIn(DataSourceType.MOCK.value, report["data_sources_in_use"])
        self.assertIn(DataSourceType.TEST.value, report["data_sources_in_use"])

        # Verify a deal was correctly sourced
        self.assertEqual(report["top_ranked_deals"][0]["data_source"], DataSourceType.LIVE.value)
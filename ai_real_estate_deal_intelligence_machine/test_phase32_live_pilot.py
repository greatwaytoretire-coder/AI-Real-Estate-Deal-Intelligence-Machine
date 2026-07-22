import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.audit_logger import AuditLogger
from ai_real_estate_deal_intelligence_machine.phase26 import ProviderManager
from ai_real_estate_deal_intelligence_machine.phase30 import (
    CanonicalProperty,
    ContinuousRuntime,
    OperatingMode,
)
from ai_real_estate_deal_intelligence_machine.phase32 import (
    LivePilotConfig,
    LivePilotRunner,
)


class Phase32LivePilotTest(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("data/test_phase32_audit.log")
        self.log_path.unlink(missing_ok=True)
        self.audit_logger = AuditLogger(log_path=self.log_path)
        provider_manager = ProviderManager(audit_logger=self.audit_logger)
        self.runtime = ContinuousRuntime(audit_logger=self.audit_logger, provider_manager=provider_manager)

    def tearDown(self):
        self.log_path.unlink(missing_ok=True)

    def test_one_market_live_pilot_workflow(self):
        """
        PHASE 32: Verify the one-market pilot workflow, including filtering and reporting.
        """
        # 1. Define the pilot configuration for Austin, TX
        config = LivePilotConfig(
            market_name="Austin, TX",
            state="TX",
            target_zip_codes=["78704", "78701"],
            property_types=["Single Family"],
            min_price=200000,
            max_price=800000,
            min_deal_score=70.0,
        )

        # 2. Create mock opportunities, some of which should be filtered out
        mock_opportunities = [
            CanonicalProperty("prop_1", "mock_provider", "rec-001", "123 main st", "78704", "fp1"),
            CanonicalProperty("prop_2", "mock_provider", "rec-002", "456 oak ave", "78701", "fp2"),
            CanonicalProperty("prop_3", "mock_provider", "rec-003", "789 pine ln", "90210", "fp3"),  # Wrong ZIP
        ]

        # 3. Initialize and run the pilot
        self.runtime.mode = OperatingMode.PILOT
        pilot_runner = LivePilotRunner(config=config, runtime=self.runtime)
        report = pilot_runner.run(mock_opportunities)

        # 4. Verify the report
        self.assertEqual(report.opportunities_processed, 2)
        self.assertEqual(report.opportunities_rejected, 1)
        self.assertEqual(report.data_mode, "PILOT")

        # 5. Verify the top-ranked opportunities
        self.assertEqual(len(report.top_ranked_opportunities), 2)
        # The deal with "123 main" should have a higher simulated score
        self.assertEqual(report.top_ranked_opportunities[0].address, "123 main st")
        self.assertEqual(report.top_ranked_opportunities[0].deal_score, 85.5)

        # 6. Verify the market ranking (heat map)
        self.assertIn("78704", report.market_ranking)
        self.assertIn("78701", report.market_ranking)
        self.assertEqual(report.market_ranking["78704"], 1)
        self.assertEqual(report.market_ranking["78701"], 1)
        # The rejected ZIP should not be in the ranking
        self.assertNotIn("90210", report.market_ranking)
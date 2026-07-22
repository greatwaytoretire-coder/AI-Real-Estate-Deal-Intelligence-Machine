import json
import tempfile
import unittest
from pathlib import Path

from ai_real_estate_deal_intelligence_machine.integration_harness import EndToEndIntegrationHarness


class Phase22IntegrationTests(unittest.TestCase):
    def test_end_to_end_pipeline_persists_and_tracks_all_stages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "phase22.db"
            log_path = Path(temp_dir) / "phase22-audit.log"
            harness = EndToEndIntegrationHarness(db_path=db_path, audit_log_path=log_path)

            trace = harness.run()

            self.assertEqual(trace["status"], "ok")
            self.assertIn("market_intelligence", trace["stages"])
            self.assertIn("property_discovery", trace["stages"])
            self.assertIn("property_intelligence", trace["stages"])
            self.assertIn("seller_signal_detection", trace["stages"])
            self.assertIn("comparable_sales", trace["stages"])
            self.assertIn("underwriting", trace["stages"])
            self.assertIn("deal_scoring", trace["stages"])
            self.assertIn("buyer_intelligence", trace["stages"])
            self.assertIn("buyer_matching", trace["stages"])
            self.assertIn("deal_packaging", trace["stages"])
            self.assertIn("acquisition_workflow", trace["stages"])
            self.assertIn("disposition_workflow", trace["stages"])
            self.assertIn("outcome_tracking", trace["stages"])
            self.assertIn("learning_system", trace["stages"])

            self.assertTrue(trace["data_flow"]["market_to_property"])
            self.assertTrue(trace["data_flow"]["property_to_underwriting"])
            self.assertTrue(trace["data_flow"]["underwriting_to_score"])
            self.assertTrue(trace["data_flow"]["score_to_buyer_match"])
            self.assertTrue(trace["data_flow"]["buyer_match_to_package"])
            self.assertTrue(trace["data_flow"]["package_to_workflow"])
            self.assertTrue(trace["data_flow"]["workflow_to_outcome"])
            self.assertTrue(trace["data_flow"]["outcome_to_learning"])

            self.assertIn("mock", trace["stages"]["market_intelligence"]["source_label"])
            self.assertIn("mock", trace["stages"]["property_discovery"]["source_label"])

            self.assertTrue(log_path.exists())
            self.assertGreater(len(trace["audit_logs"]), 0)
            self.assertGreater(len(trace["stage_records"]), 0)

    def test_pipeline_handles_stage_failure_safely(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "phase22.db"
            log_path = Path(temp_dir) / "phase22-audit.log"
            harness = EndToEndIntegrationHarness(
                db_path=db_path,
                audit_log_path=log_path,
                simulate_failure="buyer_matching",
            )

            trace = harness.run()

            self.assertEqual(trace["status"], "degraded")
            self.assertIn("buyer_matching", trace["errors"])
            self.assertIn("buyer_matching", trace["stage_results"])
            self.assertEqual(trace["stage_results"]["buyer_matching"]["status"], "error")
            self.assertTrue(trace["stage_results"]["buyer_matching"]["error"])


if __name__ == "__main__":
    unittest.main()

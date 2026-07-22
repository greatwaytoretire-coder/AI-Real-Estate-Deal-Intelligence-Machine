import unittest

from ai_real_estate_deal_intelligence_machine.phase15 import (
    LearningVersion,
    OutcomeLearningEngine,
    OutcomePerformanceReport,
)


class Phase15OutcomeLearningTests(unittest.TestCase):
    def test_learning_version_and_report_are_created(self):
        report = OutcomePerformanceReport(
            market="Austin, TX",
            estimated_arv=220000,
            actual_sale_price=230000,
            estimated_repairs=15000,
            actual_repairs=14000,
            estimated_profit=18000,
            actual_profit=19000,
            predicted_buyer_reliability=0.9,
            actual_closing_behavior=0.95,
            predicted_seller_motivation=0.75,
            actual_engagement=0.78,
            market_ranking=1,
            actual_deal_performance=1,
        )

        self.assertEqual(report.market, "Austin, TX")
        self.assertGreaterEqual(report.actual_profit, 0)

    def test_outcome_learning_engine_tracks_best_signals_and_versioning(self):
        engine = OutcomeLearningEngine()
        report = engine.generate_performance_report()
        version = engine.create_learning_version()

        self.assertIsInstance(report, OutcomePerformanceReport)
        self.assertIsInstance(version, LearningVersion)
        self.assertTrue(version.logged)
        self.assertTrue(version.explainable)
        self.assertTrue(version.reversible)


if __name__ == "__main__":
    unittest.main()

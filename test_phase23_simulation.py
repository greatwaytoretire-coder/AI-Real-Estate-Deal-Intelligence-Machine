import unittest

from ai_real_estate_deal_intelligence_machine.phase23 import (
    EndToEndDealSimulation,
    EndToEndSimulationReport,
)


class Phase23EndToEndSimulationTest(unittest.TestCase):
    def test_run_complete_end_to_end_simulation(self):
        """
        PHASE 23: Verify that a complete end-to-end deal simulation
        can run using only mock data and internal agents.
        """
        simulation = EndToEndDealSimulation()
        report = simulation.run()

        self.assertIsInstance(report, EndToEndSimulationReport)
        self.assertFalse(report.stages_failed, f"Stages failed: {report.stages_failed}")
        self.assertFalse(report.errors, f"Errors found: {report.errors}")

        expected_stages = [
            "Market Intelligence",
            "Property Discovery",
            "Seller Motivation",
            "Comparable Sales",
            "ARV Calculation",
            "Repair Estimation",
            "Underwriting",
            "Deal Scoring",
            "Risk Scoring",
            "Buyer Discovery",
            "Buyer Matching",
            "Deal Packaging",
            "Workflow Preparation",
            "Outcome Recording",
            "Learning Record Creation",
        ]
        self.assertEqual(report.stages_completed, expected_stages)

        self.assertIsNotNone(report.final_deal_score)
        self.assertIsNotNone(report.final_risk_score)
        self.assertIsNotNone(report.final_buyer_match_score)
        self.assertIsNotNone(report.final_deal_package)
        self.assertIn("Investor-Ready Package (SIMULATION)", report.final_deal_package["status"])
        self.assertTrue(report.reproducible)


if __name__ == "__main__":
    unittest.main()
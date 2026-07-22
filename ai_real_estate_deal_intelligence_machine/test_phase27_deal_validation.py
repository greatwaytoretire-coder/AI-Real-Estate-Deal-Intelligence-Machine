import unittest

from ai_real_estate_deal_intelligence_machine.phase27 import (
    DealValidationEngine,
    ValidatedDeal,
    ValidationStatus,
)


class Phase27DealValidationTest(unittest.TestCase):
    def test_deal_validation_workflow_and_reporting(self):
        """
        PHASE 27: Verify the deal validation workflow and accuracy reporting.
        """
        engine = DealValidationEngine()

        # 1. AI analyzes three deals and submits them for validation.
        deal1 = ValidatedDeal(
            deal_id="deal-001",
            ai_estimated_arv=250000,
            ai_repair_estimate=20000,
            ai_deal_score=85,
            ai_top_buyer_match="buyer-A",
        )
        deal2 = ValidatedDeal(
            deal_id="deal-002",
            ai_estimated_arv=300000,  # Overvalued
            ai_repair_estimate=15000,
            ai_deal_score=90,  # False Positive
            ai_top_buyer_match="buyer-B",
        )
        deal3 = ValidatedDeal(
            deal_id="deal-003",
            ai_estimated_arv=220000,
            ai_repair_estimate=25000,  # Underestimated
            ai_deal_score=75,
            ai_top_buyer_match="buyer-C",
        )
        engine.submit_for_validation(deal1)
        engine.submit_for_validation(deal2)
        engine.submit_for_validation(deal3)

        self.assertEqual(len(engine.validation_dataset), 3)

        # 2. A human operator reviews the deals and provides feedback.
        engine.record_feedback(
            "deal-001",
            {
                "human_arv": 255000,
                "human_repair_estimate": 22000,
                "human_assessment": "Good deal, AI is accurate.",
                "feedback_status": ValidationStatus.CORRECT,
            },
        )
        engine.record_feedback(
            "deal-002",
            {
                "human_arv": 270000,  # Lower than AI
                "human_repair_estimate": 20000,
                "human_assessment": "This is a bad deal, AI is way off.",
                "feedback_status": ValidationStatus.INCORRECT,
            },
        )

        # Deal 3 is left as PENDING_REVIEW

        # 3. The engine generates an accuracy report.
        report = engine.generate_accuracy_report()

        # 4. Verify the report metrics.
        self.assertEqual(report.opportunities_reviewed, 2)  # Only deal1 and deal2 were reviewed
        self.assertEqual(report.underwriting_accuracy, 50.0)  # Only deal1 was accurate
        self.assertEqual(report.buyer_matching_accuracy, 50.0)  # Only deal1 was correct/partially correct
        self.assertEqual(report.false_positives, 1)  # deal2 was a false positive
        self.assertEqual(report.overvalued_properties, 1)  # deal2 was overvalued
        self.assertIn("System tends to overvalue properties.", report.major_error_patterns)
        self.assertIn("Review ARV model for upward bias.", report.recommended_improvements)
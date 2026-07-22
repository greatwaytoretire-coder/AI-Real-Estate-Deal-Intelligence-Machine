import unittest

from ai_real_estate_deal_intelligence_machine.phase33 import (
    AIPrediction,
    ActualOutcome,
    LearningRecord,
    ValidationResult,
)


class Phase33DataModelTest(unittest.TestCase):
    def test_create_prediction_and_outcome_models(self):
        """
        PHASE 33: Verify the creation of prediction and outcome data models.
        """
        prediction = AIPrediction(
            deal_id="deal-001",
            deal_score=85.0,
            estimated_arv=250000,
            estimated_profit=30000,
        )
        self.assertEqual(prediction.deal_id, "deal-001")
        self.assertIsNotNone(prediction.prediction_id)

        outcome = ActualOutcome(
            deal_id="deal-001",
            deal_outcome="CLOSED",
            actual_sale_price=260000,
            actual_purchase_price=190000,
            actual_repair_costs=25000,
        )
        self.assertEqual(outcome.deal_id, "deal-001")
        self.assertEqual(outcome.actual_profit, 45000)  # 260k - 190k - 25k

    def test_validation_result_variance_calculation(self):
        """
        PHASE 33: Verify the variance calculation in the ValidationResult model.
        """
        prediction = AIPrediction(estimated_arv=250000, estimated_profit=30000)
        outcome = ActualOutcome(actual_sale_price=260000, actual_purchase_price=190000, actual_repair_costs=25000)

        validation = ValidationResult(prediction=prediction, outcome=outcome)

        # ARV Variance: (250k - 260k) / 260k = -3.84%
        self.assertAlmostEqual(validation.arv_variance_percent, -3.84, places=2)

        # Profit Variance: (30k - 45k) / 45k = -33.33%
        self.assertAlmostEqual(validation.profit_variance_percent, -33.33, places=2)

    def test_learning_record_creation(self):
        """PHASE 33: Verify the LearningRecord model can be created."""
        record = LearningRecord(deal_id="deal-001", insight="AI underestimated repair costs.")
        self.assertIsNotNone(record.learning_id)
        self.assertEqual(record.insight, "AI underestimated repair costs.")
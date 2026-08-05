from datetime import datetime, timezone

from .learning_models import DealOutcome, LearningRecord


class OutcomeTracker:

    def __init__(self):
        self.outcomes = []
        self.learning_records = []

    def record_outcome(
        self,
        deal_id,
        address,
        outcome,
        actual_profit,
        expected_profit,
    ):

        record = DealOutcome(
            deal_id=deal_id,
            address=address,
            outcome=outcome,
            actual_profit=actual_profit,
            expected_profit=expected_profit,
            completed_at=datetime.now(timezone.utc), 
        )

        self.outcomes.append(record)

        lesson = self._generate_learning(record)

        self.learning_records.append(lesson)

        return record


    def _generate_learning(self, outcome):

        difference = (
            outcome.actual_profit -
            outcome.expected_profit
        )

        if difference >= 0:
            lesson = (
                "Deal exceeded financial expectations."
            )
        else:
            lesson = (
                "Deal underperformed compared to forecast."
            )

        return LearningRecord(
            deal_id=outcome.deal_id,
            lesson=lesson,
            category="financial_performance",
            created_at=datetime.now(timezone.utc),
        )


    def get_learning_history(self):

        return self.learning_records
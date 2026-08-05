from datetime import datetime, timezone

from .feedback_models import DealFeedback


class FeedbackEngine:

    def __init__(self):
        self.feedback_records = []


    def evaluate_deal(
        self,
        deal_id,
        predicted_profit,
        actual_profit,
    ):

        accuracy = self._calculate_accuracy(
            predicted_profit,
            actual_profit,
        )

        feedback = DealFeedback(
            deal_id=deal_id,
            predicted_profit=predicted_profit,
            actual_profit=actual_profit,
            accuracy_score=accuracy,
            created_at=datetime.now(timezone.utc),
        )

        self.feedback_records.append(feedback)

        return feedback


    def _calculate_accuracy(
        self,
        predicted_profit,
        actual_profit,
    ):

        if actual_profit == 0:
            return 0.0

        difference = abs(
            predicted_profit - actual_profit
        )

        score = 1 - (
            difference / abs(actual_profit)
        )

        return max(0.0, score)


    def get_feedback_history(self):

        return self.feedback_records
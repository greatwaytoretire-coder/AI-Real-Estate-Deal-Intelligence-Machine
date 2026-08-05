from datetime import datetime, timezone

from .optimization_models import OptimizationRecommendation


class OptimizationEngine:

    def __init__(self):
        self.recommendations = []

    def evaluate_feedback(self, feedback_records):

        self.recommendations.clear()

        if not feedback_records:
            return []

        average_accuracy = (
            sum(f.accuracy_score for f in feedback_records)
            / len(feedback_records)
        )

        if average_accuracy < 0.80:

            recommendation = OptimizationRecommendation(
                category="UNDERWRITING",
                recommendation=(
                    "Increase underwriting review for "
                    "low-confidence deals."
                ),
                confidence=1.0 - average_accuracy,
                created_at=datetime.now(timezone.utc),
            )

            self.recommendations.append(recommendation)

        else:

            recommendation = OptimizationRecommendation(
                category="PERFORMANCE",
                recommendation=(
                    "Current prediction accuracy is stable."
                ),
                confidence=average_accuracy,
                created_at=datetime.now(timezone.utc),
            )

            self.recommendations.append(recommendation)

        return self.recommendations

    def get_recommendations(self):

        return self.recommendations
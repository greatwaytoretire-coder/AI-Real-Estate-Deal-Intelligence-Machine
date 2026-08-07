from __future__ import annotations

from typing import Any, Dict, Iterable


class PredictionAccuracyTracker:
    """
    Measures predictive intelligence accuracy.

    Sprint 4 Part 12:
    Continuous Intelligence Optimization.

    Compares predicted outcomes against actual
    closed deal results.
    """

    def evaluate(
        self,
        predictions: Iterable[Dict[str, Any]],
        outcomes: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Compare predictions against actual outcomes.
        """

        prediction_map = {
            prediction.get("deal_id"): prediction
            for prediction in predictions
            if isinstance(prediction, dict)
        }

        total_predictions = 0
        correct_predictions = 0
        incorrect_predictions = 0

        evaluations = []

        for outcome in outcomes:

            if not isinstance(outcome, dict):
                continue

            deal_id = outcome.get(
                "deal_id"
            )

            prediction = prediction_map.get(
                deal_id
            )

            if not prediction:
                continue

            total_predictions += 1

            predicted = prediction.get(
                "predicted_outcome"
            )

            actual = outcome.get(
                "actual_outcome"
            )

            correct = (
                predicted == actual
            )

            if correct:
                correct_predictions += 1
            else:
                incorrect_predictions += 1

            evaluations.append(
                {
                    "deal_id": deal_id,
                    "predicted_outcome": predicted,
                    "actual_outcome": actual,
                    "correct": correct,
                }
            )

        if total_predictions == 0:
            accuracy = 0.0
        else:
            accuracy = (
                correct_predictions
                / total_predictions
            ) * 100

        return {
            "total_predictions": total_predictions,
            "correct_predictions": correct_predictions,
            "incorrect_predictions": incorrect_predictions,
            "accuracy": round(
                accuracy,
                2,
            ),
            "evaluations": evaluations,
            "status": "PREDICTION_ACCURACY_EVALUATED",
        }
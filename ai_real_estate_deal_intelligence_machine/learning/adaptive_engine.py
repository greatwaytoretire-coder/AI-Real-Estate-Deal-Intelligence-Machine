from datetime import datetime, timezone
from typing import Dict, Any


class AdaptiveEngine:
    """
    Adaptive intelligence layer.

    Uses historical learning signals to improve
    future investment analysis decisions.

    Sprint 4 Part 5 Foundation:

    Learning History
          |
          v
    Confidence Evaluation
          |
          v
    Strategy Adjustment
    """

    def __init__(self):

        self.learning_history = []



    def record_learning(
        self,
        learning_event: Dict[str, Any],
    ):
        """
        Store learning events for future adaptation.
        """

        learning_event["recorded_at"] = datetime.now(
            timezone.utc
        )

        self.learning_history.append(
            learning_event
        )

        return learning_event



    def evaluate_confidence(
        self,
    ):
        """
        Calculate current learning confidence.

        Foundation model:
        More historical learning events
        increase system confidence.
        """

        total_events = len(
            self.learning_history
        )


        confidence = min(
            total_events * 10,
            100
        )


        return {

            "learning_events":
                total_events,

            "confidence":
                confidence,

        }



    def generate_strategy_adjustments(
        self,
    ):
        """
        Generate adaptive recommendations.
        """

        confidence_data = self.evaluate_confidence()


        adjustments = []


        if confidence_data["confidence"] >= 50:

            adjustments.append(
                "Increase weighting of proven acquisition signals."
            )


        else:

            adjustments.append(
                "Continue collecting deal outcome data before major strategy changes."
            )



        return {

            "confidence":
                confidence_data,

            "adjustments":
                adjustments,

            "generated_at":
                datetime.now(
                    timezone.utc
                ),

        }
    
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass
class OutcomeAnalysis:
    """
    Result of comparing predicted deal performance
    against actual deal performance.

    Used by the learning feedback system to improve
    future acquisition decisions.
    """

    deal_id: str

    prediction_accuracy: float

    profit_accuracy: float

    recommendation_accuracy: bool

    lessons: list[str]

    analyzed_at: datetime



class OutcomeAnalyzer:
    """
    Analyzes completed deals.

    Compares:

    Predicted:
        - projected profit
        - recommendation
        - deal score

    Actual:
        - realized profit
        - closing result

    Produces learning feedback.
    """



    def analyze(
        self,
        prediction: Dict[str, Any],
        actual: Dict[str, Any],
    ) -> OutcomeAnalysis:
        """
        Compare predicted investment outcome
        with actual investment outcome.
        """



        deal_id = prediction.get(
            "deal_id",
            "UNKNOWN",
        )



        projected_profit = float(
            prediction.get(
                "projected_profit",
                0,
            )
        )


        actual_profit = float(
            actual.get(
                "actual_profit",
                0,
            )
        )



        predicted_recommendation = prediction.get(
            "recommendation",
            "UNKNOWN",
        )


        actual_recommendation = actual.get(
            "recommendation",
            predicted_recommendation,
        )



        # ---------------------------------------
        # Profit Accuracy
        # ---------------------------------------

        if projected_profit == 0:

            profit_accuracy = 0.0

        else:

            profit_accuracy = (
                actual_profit
                /
                projected_profit
            ) * 100



        profit_accuracy = round(
            min(
                profit_accuracy,
                100,
            ),
            2,
        )



        # ---------------------------------------
        # Recommendation Accuracy
        # ---------------------------------------

        recommendation_accuracy = (
            predicted_recommendation
            ==
            actual_recommendation
        )



        # ---------------------------------------
        # Overall Prediction Accuracy
        # ---------------------------------------

        prediction_accuracy = round(

            (
                profit_accuracy
                +
                (
                    100
                    if recommendation_accuracy
                    else 0
                )

            )
            /
            2,

            2,

        )



        # ---------------------------------------
        # Learning Lessons
        # ---------------------------------------

        lessons = []



        if profit_accuracy >= 90:

            lessons.append(
                "Profit projections were highly accurate."
            )


        elif profit_accuracy >= 60:

            lessons.append(
                "Profit projections were moderately accurate."
            )


        else:

            lessons.append(
                "Profit projections require adjustment."
            )



        if recommendation_accuracy:

            lessons.append(
                "Acquisition recommendation was validated."
            )

        else:

            lessons.append(
                "Recommendation model requires improvement."
            )



        if actual_profit > projected_profit:

            lessons.append(
                "Deal exceeded expected profitability."
            )


        elif actual_profit < projected_profit:

            lessons.append(
                "Future underwriting should reduce profit assumptions."
            )



        return OutcomeAnalysis(

            deal_id=deal_id,

            prediction_accuracy=prediction_accuracy,

            profit_accuracy=profit_accuracy,

            recommendation_accuracy=recommendation_accuracy,

            lessons=lessons,

            analyzed_at=datetime.now(
                timezone.utc
            ),

        )
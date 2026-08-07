from __future__ import annotations

from typing import Any, Dict, List


class OutcomeLearningIntegration:
    """
    Connects acquisition outcomes back into learning intelligence.

    Sprint 4 Part 18:
    Outcome Feedback Loop
    """

    def analyze_outcomes(
        self,
        outcomes: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze completed acquisition outcomes.
        """

        total = len(
            outcomes
        )

        successful = len(
            [
                outcome
                for outcome in outcomes
                if outcome.get(
                    "success",
                    False,
                )
            ]
        )


        failed = (
            total - successful
        )


        success_rate = 0


        if total > 0:

            success_rate = round(
                (
                    successful
                    /
                    total
                )
                *
                100,
                2,
            )


        learning_adjustment = (
            "INCREASE_CONFIDENCE"
            if success_rate >= 70
            else
            "REVIEW_DECISION_SIGNALS"
        )


        return {

            "total_outcomes":
                total,

            "successful_outcomes":
                successful,

            "failed_outcomes":
                failed,

            "success_rate":
                success_rate,

            "learning_adjustment":
                learning_adjustment,

            "status":
                "OUTCOME_LEARNING_ANALYZED",

        }



    def generate_learning_signal(
        self,
        analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate feedback signal.
        """

        return {

            "success_rate":
                analysis.get(
                    "success_rate",
                    0,
                ),

            "adjustment":
                analysis.get(
                    "learning_adjustment",
                    "NO_CHANGE",
                ),

            "signal_strength":
                (
                    "HIGH"
                    if analysis.get(
                        "success_rate",
                        0,
                    ) >= 80
                    else
                    "MEDIUM"
                ),

            "status":
                "LEARNING_SIGNAL_GENERATED",

        }
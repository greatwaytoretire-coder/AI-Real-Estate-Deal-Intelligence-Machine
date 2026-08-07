from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


class AcquisitionOutcomeTracker:
    """
    Tracks acquisition execution outcomes.

    Sprint 4 Part 18:

    Execution
        |
        v
    Outcome Tracking
        |
        v
    Learning Feedback
    """

    def __init__(self) -> None:

        self.outcomes: List[Dict[str, Any]] = []


    def record_outcome(
        self,
        outcome_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Record acquisition outcome.
        """

        record = {

            "deal_id":
                outcome_data.get(
                    "deal_id",
                    "UNKNOWN",
                ),

            "decision":
                outcome_data.get(
                    "decision",
                    "UNKNOWN",
                ),

            "seller_response":
                outcome_data.get(
                    "seller_response",
                    "UNKNOWN",
                ),

            "negotiation_result":
                outcome_data.get(
                    "negotiation_result",
                    "UNKNOWN",
                ),

            "final_outcome":
                outcome_data.get(
                    "final_outcome",
                    "UNKNOWN",
                ),

            "success":
                outcome_data.get(
                    "success",
                    False,
                ),

            "recorded_at":
                datetime.now(
                    timezone.utc
                ),

            "status":
                "ACQUISITION_OUTCOME_RECORDED",

        }


        self.outcomes.append(
            record
        )


        return record



    def get_outcomes(self) -> List[Dict[str, Any]]:
        """
        Return stored acquisition outcomes.
        """

        return self.outcomes



    def summary(self) -> Dict[str, Any]:
        """
        Generate outcome summary.
        """

        total = len(
            self.outcomes
        )


        successful = len(
            [
                outcome
                for outcome in self.outcomes
                if outcome["success"]
            ]
        )


        failed = (
            total - successful
        )


        accuracy = 0

        if total > 0:
            accuracy = round(
                (successful / total) * 100,
                2,
            )


        return {

            "total_outcomes":
                total,

            "successful_outcomes":
                successful,

            "failed_outcomes":
                failed,

            "success_rate":
                accuracy,

            "status":
                "OUTCOME_SUMMARY_GENERATED",

        }
        
from __future__ import annotations

from typing import Any, Dict, List


class AcquisitionProgressAnalyzer:
    """
    Analyzes acquisition milestone execution state and identifies
    progress conditions and exceptions.
    """

    STATUS_COMPLETE = "ACQUISITION_PROGRESS_ANALYZED"

    def analyze(
        self,
        milestone_results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        analyses: List[Dict[str, Any]] = []

        for result in milestone_results:
            analyses.append(self._analyze_acquisition(result))

        normal_count = sum(
            1 for item in analyses
            if item["progress_status"] == "NORMAL_PROGRESS"
        )
        stalled_count = sum(
            1 for item in analyses
            if item["progress_status"] == "STALLED"
        )
        blocked_count = sum(
            1 for item in analyses
            if item["progress_status"] == "BLOCKED"
        )
        review_count = sum(
            1 for item in analyses
            if item["progress_status"] == "REVIEW_REQUIRED"
        )
        ready_count = sum(
            1 for item in analyses
            if item["progress_status"] == "READY_TO_ADVANCE"
        )

        return {
            "analyses": analyses,
            "summary": {
                "total_acquisitions": len(analyses),
                "normal_count": normal_count,
                "stalled_count": stalled_count,
                "blocked_count": blocked_count,
                "review_count": review_count,
                "ready_to_advance_count": ready_count,
            },
            "status": self.STATUS_COMPLETE,
        }

    def _analyze_acquisition(
        self,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        deal_id = result.get("deal_id")
        execution_state = result.get("execution_state")
        execution_status = result.get("execution_status")
        milestones = result.get("milestones", [])
        current_milestone = result.get("current_milestone")
        completed_count = result.get("completed_count", 0)
        milestone_count = result.get("milestone_count", len(milestones))

        if execution_state == "ACQUISITION_BLOCKED":
            progress_status = "BLOCKED"
            exception_type = "ACQUISITION_BLOCKED"
            recommendation = (
                "Do not advance the acquisition until the blocking "
                "condition is resolved."
            )

        elif execution_status in {
            "EXECUTION_BLOCKED",
            "ACQUISITION_BLOCKED",
        }:
            progress_status = "BLOCKED"
            exception_type = "EXECUTION_BLOCKED"
            recommendation = (
                "Resolve the execution block before continuing acquisition."
            )

        elif execution_status == "MILESTONE_ADVANCED":
            progress_status = "NORMAL_PROGRESS"
            exception_type = None
            recommendation = (
                "Acquisition is progressing normally through its milestone plan."
            )

        elif execution_state == "ACQUISITION_ACTIVE":
            if completed_count >= milestone_count and milestone_count > 0:
                progress_status = "READY_TO_ADVANCE"
                exception_type = None
                recommendation = (
                    "All acquisition milestones are complete. "
                    "Prepare the acquisition for completion."
                )
            elif current_milestone:
                progress_status = "NORMAL_PROGRESS"
                exception_type = None
                recommendation = (
                    "Continue execution of the current acquisition milestone."
                )
            else:
                progress_status = "REVIEW_REQUIRED"
                exception_type = "MISSING_CURRENT_MILESTONE"
                recommendation = (
                    "Review the acquisition because no current milestone "
                    "is identified."
                )

        else:
            progress_status = "REVIEW_REQUIRED"
            exception_type = "UNKNOWN_EXECUTION_STATE"
            recommendation = (
                "Review the acquisition because its execution state "
                "cannot be classified automatically."
            )

        return {
            "deal_id": deal_id,
            "execution_state": execution_state,
            "execution_status": execution_status,
            "current_milestone": current_milestone,
            "completed_count": completed_count,
            "milestone_count": milestone_count,
            "progress_status": progress_status,
            "exception_type": exception_type,
            "recommendation": recommendation,
            "status": "ACQUISITION_PROGRESS_CLASSIFIED",
        }
from __future__ import annotations

from typing import Any, Dict, List

from .acquisition_progress_analyzer import AcquisitionProgressAnalyzer


class AcquisitionProgressIntegration:
    """
    Integrates acquisition milestone execution results with
    progress and exception analysis.
    """

    STATUS_COMPLETE = "ACQUISITION_PROGRESS_INTEGRATION_COMPLETE"

    def __init__(
        self,
        analyzer: AcquisitionProgressAnalyzer | None = None,
    ) -> None:
        self.analyzer = analyzer or AcquisitionProgressAnalyzer()

    def evaluate(
        self,
        milestone_results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        progress = self.analyzer.analyze(milestone_results)

        analyses = progress["analyses"]

        normal_progress = [
            item
            for item in analyses
            if item["progress_status"] == "NORMAL_PROGRESS"
        ]

        stalled = [
            item
            for item in analyses
            if item["progress_status"] == "STALLED"
        ]

        blocked = [
            item
            for item in analyses
            if item["progress_status"] == "BLOCKED"
        ]

        review_required = [
            item
            for item in analyses
            if item["progress_status"] == "REVIEW_REQUIRED"
        ]

        ready_to_advance = [
            item
            for item in analyses
            if item["progress_status"] == "READY_TO_ADVANCE"
        ]

        return {
            "progress": progress,
            "normal_progress": normal_progress,
            "stalled": stalled,
            "blocked": blocked,
            "review_required": review_required,
            "ready_to_advance": ready_to_advance,
            "status": self.STATUS_COMPLETE,
        }
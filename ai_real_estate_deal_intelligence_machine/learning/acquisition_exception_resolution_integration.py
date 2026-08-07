from __future__ import annotations

from typing import Any, Dict, List

from ai_real_estate_deal_intelligence_machine.learning.acquisition_exception_resolution_engine import (
    AcquisitionExceptionResolutionEngine,
)


class AcquisitionExceptionResolutionIntegration:
    """
    Integrates Sprint 4 Part 25 acquisition progress analysis
    with Sprint 4 Part 26 exception resolution intelligence.
    """

    STATUS = "ACQUISITION_EXCEPTION_RESOLUTION_INTEGRATION_COMPLETE"

    def __init__(
        self,
        engine: AcquisitionExceptionResolutionEngine | None = None,
    ) -> None:
        self.engine = engine or AcquisitionExceptionResolutionEngine()

    def evaluate(
        self,
        progress_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        analyses = progress_result.get("progress", {}).get(
            "analyses",
            [],
        )

        if not isinstance(analyses, list):
            analyses = []

        resolution_result = self.engine.resolve(analyses)

        resolutions = resolution_result.get("resolutions", [])

        return {
            "progress_result": progress_result,
            "resolution": resolution_result,
            "action_required": [
                item
                for item in resolutions
                if item["resolution_status"] == "ACTION_REQUIRED"
            ],
            "human_review_required": [
                item
                for item in resolutions
                if item["requires_human_review"]
            ],
            "ready_to_advance": [
                item
                for item in resolutions
                if item["resolution_type"]
                == "MILESTONE_ADVANCEMENT"
            ],
            "normal_continuation": [
                item
                for item in resolutions
                if item["resolution_type"]
                == "NORMAL_ACQUISITION_CONTINUATION"
            ],
            "status": self.STATUS,
        }
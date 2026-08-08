from __future__ import annotations

from typing import Any, Dict, List

from .acquisition_action_execution_engine import (
    AcquisitionActionExecutionEngine,
)


class AcquisitionActionExecutionIntegration:
    """
    Integration layer between acquisition exception-resolution intelligence
    and controlled action execution.

    The integration consumes Part 26 resolution results and delegates
    execution classification to the Part 27 action execution engine.
    """

    def __init__(self) -> None:
        self.engine = AcquisitionActionExecutionEngine()

    def process_resolution_result(
        self,
        resolution_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process the resolution output produced by Sprint 4 Part 26.
        """

        resolution = resolution_result.get("resolution", {})

        resolutions = resolution.get("resolutions", [])

        if not resolutions:
            return {
                "executions": [],
                "automatic_execution": [],
                "human_review_required": [],
                "rejected": [],
                "summary": {
                    "total_executions": 0,
                    "automatic_execution_count": 0,
                    "human_review_count": 0,
                    "rejected_count": 0,
                },
                "status": "NO_ACQUISITION_ACTIONS_AVAILABLE",
            }

        return self.process_resolutions(resolutions)

    def process_resolutions(
        self,
        resolutions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Process a collection of acquisition resolutions."""

        execution_result = self.engine.execute_resolutions(resolutions)

        automatic_execution = execution_result["automatic_execution"]
        human_review = execution_result["human_review_required"]
        rejected = execution_result["rejected"]

        return {
            "executions": execution_result["executions"],
            "automatic_execution": automatic_execution,
            "human_review_required": human_review,
            "rejected": rejected,
            "summary": execution_result["summary"],
            "status": "ACQUISITION_ACTION_EXECUTION_INTEGRATION_COMPLETE",
        }

    def get_automatic_execution_actions(
        self,
        result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Return only actions explicitly permitted for automation."""

        return [
            execution
            for execution in result.get("automatic_execution", [])
            if execution.get("automated_execution_allowed") is True
            and execution.get("requires_human_review") is False
        ]

    def get_human_review_actions(
        self,
        result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Return actions that must remain under human control."""

        return [
            execution
            for execution in result.get("human_review_required", [])
            if execution.get("requires_human_review") is True
        ]

    def get_execution_summary(
        self,
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return the execution summary."""

        return dict(
            result.get(
                "summary",
                {
                    "total_executions": 0,
                    "automatic_execution_count": 0,
                    "human_review_count": 0,
                    "rejected_count": 0,
                },
            )
        )
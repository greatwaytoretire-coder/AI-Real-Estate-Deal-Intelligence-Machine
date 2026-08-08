from __future__ import annotations

from typing import Any, Dict, List


class AcquisitionActionExecutionEngine:
    """
    Converts acquisition exception-resolution decisions into controlled
    execution instructions.

    This layer does not perform external side effects. It determines:
    - what action should be taken,
    - whether that action is automatically executable,
    - whether human review is required,
    - what execution state should be assigned,
    - and what the next workflow step should be.
    """

    ACTION_MAP = {
        "CONTINUE_CURRENT_MILESTONE": {
            "execution_type": "AUTOMATED_CONTINUATION",
            "execution_status": "READY_FOR_EXECUTION",
            "execution_state": "ACQUISITION_EXECUTION_READY",
            "next_step": "Continue execution of the current acquisition milestone.",
            "requires_human_review": False,
            "automated_execution_allowed": True,
        },
        "ADVANCE_ACQUISITION_MILESTONE": {
            "execution_type": "AUTOMATED_MILESTONE_ADVANCEMENT",
            "execution_status": "READY_FOR_EXECUTION",
            "execution_state": "ACQUISITION_MILESTONE_ADVANCEMENT_READY",
            "next_step": "Advance the acquisition to the next milestone.",
            "requires_human_review": False,
            "automated_execution_allowed": True,
        },
        "RESOLVE_BLOCKING_CONDITION": {
            "execution_type": "BLOCKING_CONDITION_RESOLUTION",
            "execution_status": "HUMAN_ACTION_REQUIRED",
            "execution_state": "ACQUISITION_BLOCKED",
            "next_step": (
                "Identify and resolve the blocking condition before "
                "additional acquisition execution."
            ),
            "requires_human_review": True,
            "automated_execution_allowed": False,
        },
        "RECOVER_STALLED_ACQUISITION": {
            "execution_type": "STALLED_ACQUISITION_RECOVERY",
            "execution_status": "HUMAN_ACTION_REQUIRED",
            "execution_state": "ACQUISITION_RECOVERY_REQUIRED",
            "next_step": (
                "Investigate the stalled milestone and initiate a "
                "recovery action."
            ),
            "requires_human_review": True,
            "automated_execution_allowed": False,
        },
        "ROUTE_TO_HUMAN_REVIEW": {
            "execution_type": "HUMAN_REVIEW_ROUTING",
            "execution_status": "HUMAN_REVIEW_REQUIRED",
            "execution_state": "ACQUISITION_REVIEW_REQUIRED",
            "next_step": (
                "Route the acquisition to human review before "
                "additional execution occurs."
            ),
            "requires_human_review": True,
            "automated_execution_allowed": False,
        },
    }

    def __init__(self) -> None:
        self.execution_history: List[Dict[str, Any]] = []

    def execute_resolution(
        self,
        resolution: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Convert one resolution into a controlled execution instruction."""

        deal_id = resolution.get("deal_id")
        action = resolution.get("resolution_action")

        if not deal_id:
            return {
                "deal_id": deal_id,
                "status": "INVALID_EXECUTION_REQUEST",
                "execution_status": "EXECUTION_REJECTED",
                "execution_action": action,
                "reason": "Missing deal_id.",
            }

        if action not in self.ACTION_MAP:
            return {
                "deal_id": deal_id,
                "status": "INVALID_EXECUTION_REQUEST",
                "execution_status": "EXECUTION_REJECTED",
                "execution_action": action,
                "reason": "Unsupported acquisition resolution action.",
            }

        action_config = self.ACTION_MAP[action]

        result = {
            "deal_id": deal_id,
            "current_milestone": resolution.get("current_milestone"),
            "progress_status": resolution.get("progress_status"),
            "exception_type": resolution.get("exception_type"),
            "resolution_type": resolution.get("resolution_type"),
            "resolution_action": action,
            "execution_type": action_config["execution_type"],
            "execution_state": action_config["execution_state"],
            "execution_status": action_config["execution_status"],
            "next_step": action_config["next_step"],
            "requires_human_review": action_config["requires_human_review"],
            "automated_execution_allowed": action_config[
                "automated_execution_allowed"
            ],
            "status": "ACQUISITION_ACTION_EXECUTION_GENERATED",
        }

        self._enforce_execution_safety(result)

        self.execution_history.append(result)

        return result

    def execute_resolutions(
        self,
        resolutions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Convert a collection of resolutions into execution instructions."""

        executions = [
            self.execute_resolution(resolution)
            for resolution in resolutions
        ]

        automatic_execution = [
            execution
            for execution in executions
            if execution.get("automated_execution_allowed") is True
        ]

        human_review = [
            execution
            for execution in executions
            if execution.get("requires_human_review") is True
        ]

        rejected = [
            execution
            for execution in executions
            if execution.get("execution_status") == "EXECUTION_REJECTED"
        ]

        return {
            "executions": executions,
            "automatic_execution": automatic_execution,
            "human_review_required": human_review,
            "rejected": rejected,
            "summary": {
                "total_executions": len(executions),
                "automatic_execution_count": len(automatic_execution),
                "human_review_count": len(human_review),
                "rejected_count": len(rejected),
            },
            "status": "ACQUISITION_ACTION_EXECUTION_COMPLETE",
        }

    def _enforce_execution_safety(
        self,
        execution: Dict[str, Any],
    ) -> None:
        """
        Prevent blocked/review-required resolutions from becoming
        automatically executable.
        """

        exception_type = execution.get("exception_type")
        progress_status = execution.get("progress_status")
        action = execution.get("resolution_action")

        protected_conditions = {
            "ACQUISITION_BLOCKED",
            "MILESTONE_STALLED",
            "MANUAL_REVIEW_REQUIRED",
        }

        protected_progress = {
            "BLOCKED",
            "STALLED",
            "REVIEW_REQUIRED",
        }

        if (
            exception_type in protected_conditions
            or progress_status in protected_progress
        ):
            execution["requires_human_review"] = True
            execution["automated_execution_allowed"] = False

        if action in {
            "RESOLVE_BLOCKING_CONDITION",
            "RECOVER_STALLED_ACQUISITION",
            "ROUTE_TO_HUMAN_REVIEW",
        }:
            execution["requires_human_review"] = True
            execution["automated_execution_allowed"] = False

        if (
            execution["requires_human_review"]
            and execution["automated_execution_allowed"]
        ):
            execution["automated_execution_allowed"] = False

        if execution["automated_execution_allowed"]:
            execution["execution_status"] = "READY_FOR_EXECUTION"
        else:
            if execution["requires_human_review"]:
                execution["execution_status"] = (
                    "HUMAN_REVIEW_REQUIRED"
                    if action == "ROUTE_TO_HUMAN_REVIEW"
                    else "HUMAN_ACTION_REQUIRED"
                )

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Return a copy of generated execution instructions."""

        return list(self.execution_history)
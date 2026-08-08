from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass(frozen=True)
class RecoveryActionPlan:
    """Represents a controlled plan for recovering an acquisition outcome."""

    deal_id: str
    execution_status: str
    source_outcome_status: str
    source_verification_status: str
    source_resolution_status: str
    source_resolution_action: str
    recovery_required: bool
    requires_human_review: bool
    automated_planning_allowed: bool
    planning_status: str
    recovery_action: str
    recovery_reason: str
    next_step: str
    state_transition: str
    execution_authorization_required: bool
    status: str = "ACQUISITION_RECOVERY_ACTION_PLAN_CREATED"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AcquisitionRecoveryActionPlanner:
    """
    Creates controlled recovery action plans from verified acquisition
    outcome-resolution results.

    This component plans recovery actions only. It does not execute
    acquisition actions and does not grant execution authority.
    """

    STATUS_COMPLETE = "ACQUISITION_RECOVERY_ACTION_PLANNING_COMPLETE"

    def plan_recovery_action(
        self,
        resolution: Dict[str, Any],
    ) -> RecoveryActionPlan:
        deal_id = str(resolution.get("deal_id", ""))

        execution_status = str(
            resolution.get("execution_status", "")
        )

        source_outcome_status = str(
            resolution.get("source_outcome_status", "")
        )

        source_verification_status = str(
            resolution.get("source_verification_status", "")
        )

        source_resolution_status = str(
            resolution.get("resolution_status", "")
        )

        source_resolution_action = str(
            resolution.get("resolution_action", "")
        )

        recovery_required = bool(
            resolution.get("recovery_required", False)
        )

        requires_human_review = bool(
            resolution.get("requires_human_review", False)
        )

        state_transition = str(
            resolution.get("state_transition", "")
        )

        if not deal_id:
            raise ValueError("Recovery planning requires a deal_id.")

        if source_verification_status == "STATE_MISMATCH":
            return RecoveryActionPlan(
                deal_id=deal_id,
                execution_status=execution_status,
                source_outcome_status=source_outcome_status,
                source_verification_status=source_verification_status,
                source_resolution_status=source_resolution_status,
                source_resolution_action=source_resolution_action,
                recovery_required=True,
                requires_human_review=True,
                automated_planning_allowed=True,
                planning_status="PLANNED_FOR_HUMAN_INVESTIGATION",
                recovery_action="INVESTIGATE_STATE_MISMATCH",
                recovery_reason=(
                    "The verified acquisition state does not match the "
                    "expected state transition."
                ),
                next_step=(
                    "Stop additional automated acquisition execution and "
                    "route the state mismatch for controlled human "
                    "investigation."
                ),
                state_transition=(
                    state_transition
                    or "ACQUISITION_REMAINS_REVIEW_REQUIRED"
                ),
                execution_authorization_required=True,
            )

        if (
            source_verification_status == "FAILED"
            or source_outcome_status == "EXECUTION_FAILED"
        ):
            return RecoveryActionPlan(
                deal_id=deal_id,
                execution_status=execution_status,
                source_outcome_status=source_outcome_status,
                source_verification_status=source_verification_status,
                source_resolution_status=source_resolution_status,
                source_resolution_action=source_resolution_action,
                recovery_required=True,
                requires_human_review=True,
                automated_planning_allowed=True,
                planning_status="PLANNED_FOR_FAILED_EXECUTION_RECOVERY",
                recovery_action="RECOVER_FAILED_EXECUTION",
                recovery_reason=(
                    "The acquisition action failed and requires "
                    "controlled recovery before execution can continue."
                ),
                next_step=(
                    "Stop additional automated execution and create a "
                    "controlled recovery workflow for the failed action."
                ),
                state_transition=(
                    state_transition
                    or "ACQUISITION_REMAINS_RECOVERY_REQUIRED"
                ),
                execution_authorization_required=True,
            )

        if source_outcome_status == "REJECTED":
            return RecoveryActionPlan(
                deal_id=deal_id,
                execution_status=execution_status,
                source_outcome_status=source_outcome_status,
                source_verification_status=source_verification_status,
                source_resolution_status=source_resolution_status,
                source_resolution_action=source_resolution_action,
                recovery_required=False,
                requires_human_review=True,
                automated_planning_allowed=False,
                planning_status="NO_RECOVERY_ACTION_AUTHORIZED",
                recovery_action="PRESERVE_REJECTED_STATE",
                recovery_reason=(
                    "The source action was rejected and must not be "
                    "re-executed through the recovery planner."
                ),
                next_step=(
                    "Preserve the rejected state and route the matter "
                    "through the appropriate human review process."
                ),
                state_transition=(
                    state_transition or "NO_STATE_CHANGE"
                ),
                execution_authorization_required=True,
            )

        if requires_human_review:
            return RecoveryActionPlan(
                deal_id=deal_id,
                execution_status=execution_status,
                source_outcome_status=source_outcome_status,
                source_verification_status=source_verification_status,
                source_resolution_status=source_resolution_status,
                source_resolution_action=source_resolution_action,
                recovery_required=recovery_required,
                requires_human_review=True,
                automated_planning_allowed=False,
                planning_status="DEFERRED_TO_HUMAN_CONTROL",
                recovery_action="MAINTAIN_HUMAN_CONTROL",
                recovery_reason=(
                    "The resolved acquisition outcome remains under "
                    "human control."
                ),
                next_step=(
                    "Maintain the current acquisition state until the "
                    "required human action has been completed."
                ),
                state_transition=state_transition,
                execution_authorization_required=True,
            )

        if (
            source_resolution_action == "CONTINUE_ACQUISITION"
            and source_verification_status == "SUCCESS"
        ):
            return RecoveryActionPlan(
                deal_id=deal_id,
                execution_status=execution_status,
                source_outcome_status=source_outcome_status,
                source_verification_status=source_verification_status,
                source_resolution_status=source_resolution_status,
                source_resolution_action=source_resolution_action,
                recovery_required=False,
                requires_human_review=False,
                automated_planning_allowed=True,
                planning_status="NO_RECOVERY_REQUIRED",
                recovery_action="CONTINUE_ACQUISITION",
                recovery_reason=(
                    "The acquisition outcome was successfully verified "
                    "and resolved without a recovery condition."
                ),
                next_step=(
                    "Continue the previously authorized acquisition "
                    "workflow."
                ),
                state_transition=state_transition,
                execution_authorization_required=False,
            )

        if (
            source_resolution_action == "PROCEED_TO_NEXT_MILESTONE"
            and source_verification_status == "SUCCESS"
        ):
            return RecoveryActionPlan(
                deal_id=deal_id,
                execution_status=execution_status,
                source_outcome_status=source_outcome_status,
                source_verification_status=source_verification_status,
                source_resolution_status=source_resolution_status,
                source_resolution_action=source_resolution_action,
                recovery_required=False,
                requires_human_review=False,
                automated_planning_allowed=True,
                planning_status="NO_RECOVERY_REQUIRED",
                recovery_action="PROCEED_TO_NEXT_MILESTONE",
                recovery_reason=(
                    "The acquisition milestone was successfully "
                    "verified and approved for continuation."
                ),
                next_step=(
                    "Proceed through the next previously authorized "
                    "acquisition milestone."
                ),
                state_transition=state_transition,
                execution_authorization_required=False,
            )

        return RecoveryActionPlan(
            deal_id=deal_id,
            execution_status=execution_status,
            source_outcome_status=source_outcome_status,
            source_verification_status=source_verification_status,
            source_resolution_status=source_resolution_status,
            source_resolution_action=source_resolution_action,
            recovery_required=True,
            requires_human_review=True,
            automated_planning_allowed=False,
            planning_status="ESCALATED_FOR_REVIEW",
            recovery_action="INVESTIGATE_UNCLASSIFIED_OUTCOME",
            recovery_reason=(
                "The acquisition outcome could not be safely classified "
                "into an approved recovery pathway."
            ),
            next_step=(
                "Stop additional automated execution and route the "
                "outcome for controlled human review."
            ),
            state_transition=(
                state_transition
                or "ACQUISITION_REMAINS_REVIEW_REQUIRED"
            ),
            execution_authorization_required=True,
        )

    def plan_from_resolutions(
        self,
        resolution_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not isinstance(resolution_results, dict):
            raise TypeError("Resolution results must be a dictionary.")

        resolutions = resolution_results.get("resolutions", [])

        if not isinstance(resolutions, list):
            raise TypeError("Resolution results must contain a list.")

        plans: List[Dict[str, Any]] = []

        for resolution in resolutions:
            if not isinstance(resolution, dict):
                raise TypeError(
                    "Each resolution must be a dictionary."
                )

            plan = self.plan_recovery_action(resolution)
            plans.append(plan.to_dict())

        automatic_plans = [
            plan
            for plan in plans
            if plan["automated_planning_allowed"]
        ]

        human_required = [
            plan
            for plan in plans
            if plan["requires_human_review"]
        ]

        recovery_required_plans = [
            plan
            for plan in plans
            if plan["recovery_required"]
        ]

        return {
            "source_status": resolution_results.get("status"),
            "status": self.STATUS_COMPLETE,
            "plans": plans,
            "automatic_plans": automatic_plans,
            "human_required": human_required,
            "recovery_required": recovery_required_plans,
            "summary": {
                "total_outcomes": len(plans),
                "automatic_plan_count": len(automatic_plans),
                "human_review_count": len(human_required),
                "recovery_required_count": len(
                    recovery_required_plans
                ),
            },
        }
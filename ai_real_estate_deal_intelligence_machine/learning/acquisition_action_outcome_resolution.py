from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class AcquisitionOutcomeResolution:
    deal_id: str
    resolution_action: str
    resolution_status: str
    source_outcome_status: str
    source_verification_status: str
    state_transition: str
    next_step: str
    automated_resolution_allowed: bool
    requires_human_review: bool
    recovery_required: bool
    status: str


class AcquisitionActionOutcomeResolver:
    """
    Resolves verified acquisition action outcomes into the next
    controlled acquisition response.

    This layer does not execute the next action. It determines what
    should happen next after Part 29 outcome verification.
    """

    STATUS = "ACQUISITION_ACTION_OUTCOME_RESOLUTION_COMPLETE"

    def resolve(self, verification: Dict[str, Any]) -> Dict[str, Any]:
        verifications = verification.get("verifications", [])

        resolutions: List[Dict[str, Any]] = []

        for outcome in verifications:
            resolutions.append(self._resolve_outcome(outcome))

        automatic = [
            item
            for item in resolutions
            if item["automated_resolution_allowed"]
        ]

        human_required = [
            item
            for item in resolutions
            if item["requires_human_review"]
        ]

        recovery_required = [
            item
            for item in resolutions
            if item["recovery_required"]
        ]

        return {
            "source_status": verification.get("status"),
            "status": self.STATUS,
            "resolutions": resolutions,
            "automatic_resolutions": automatic,
            "human_required": human_required,
            "recovery_required": recovery_required,
            "summary": {
                "total_outcomes": len(resolutions),
                "automatic_resolution_count": len(automatic),
                "human_review_count": len(human_required),
                "recovery_required_count": len(recovery_required),
            },
        }

    def _resolve_outcome(
        self,
        outcome: Dict[str, Any],
    ) -> Dict[str, Any]:
        deal_id = outcome.get("deal_id")
        outcome_status = outcome.get("outcome_status")
        verification_status = outcome.get("verification_status")
        execution_status = outcome.get("execution_status")
        state_transition = outcome.get("actual_state_transition")
        resolution_action = outcome.get("resolution_action")

        if verification_status == "STATE_MISMATCH":
            return self._build_resolution(
                outcome=outcome,
                resolution_action="INVESTIGATE_STATE_MISMATCH",
                resolution_status="ESCALATED",
                next_step=(
                    "Stop additional automated acquisition execution "
                    "and investigate the state mismatch."
                ),
                automated_resolution_allowed=False,
                requires_human_review=True,
                recovery_required=True,
                state_transition="ACQUISITION_REMAINS_REVIEW_REQUIRED",
            )

        if verification_status == "FAILED":
            return self._build_resolution(
                outcome=outcome,
                resolution_action="RECOVER_FAILED_EXECUTION",
                resolution_status="RECOVERY_REQUIRED",
                next_step=(
                    "Stop additional automated execution and initiate "
                    "controlled recovery of the failed acquisition action."
                ),
                automated_resolution_allowed=False,
                requires_human_review=True,
                recovery_required=True,
                state_transition="ACQUISITION_REMAINS_RECOVERY_REQUIRED",
            )

        if execution_status == "REJECTED":
            return self._build_resolution(
                outcome=outcome,
                resolution_action="PRESERVE_REJECTED_STATE",
                resolution_status="REJECTED",
                next_step=(
                    "Preserve the current acquisition state and route "
                    "the rejected action for human review."
                ),
                automated_resolution_allowed=False,
                requires_human_review=True,
                recovery_required=False,
                state_transition="NO_STATE_CHANGE",
            )

        if outcome_status == "DEFERRED_TO_HUMAN":
            return self._build_resolution(
                outcome=outcome,
                resolution_action="MAINTAIN_HUMAN_CONTROL",
                resolution_status="DEFERRED",
                next_step=(
                    "Maintain the current acquisition state until "
                    "required human action is completed."
                ),
                automated_resolution_allowed=False,
                requires_human_review=True,
                recovery_required=False,
                state_transition=state_transition,
            )

        if (
            verification_status == "SUCCESS"
            and outcome_status == "EXECUTION_SUCCESSFUL"
            and resolution_action == "CONTINUE_CURRENT_MILESTONE"
        ):
            return self._build_resolution(
                outcome=outcome,
                resolution_action="CONTINUE_ACQUISITION",
                resolution_status="CONTINUED",
                next_step=(
                    "Continue the current acquisition milestone "
                    "under the previously authorized workflow."
                ),
                automated_resolution_allowed=True,
                requires_human_review=False,
                recovery_required=False,
                state_transition="ACQUISITION_REMAINS_ACTIVE",
            )

        if (
            verification_status == "SUCCESS"
            and outcome_status == "EXECUTION_SUCCESSFUL"
            and resolution_action == "ADVANCE_ACQUISITION_MILESTONE"
        ):
            return self._build_resolution(
                outcome=outcome,
                resolution_action="PROCEED_TO_NEXT_MILESTONE",
                resolution_status="ADVANCE_APPROVED",
                next_step=(
                    "Proceed to the next acquisition milestone using "
                    "the verified acquisition state."
                ),
                automated_resolution_allowed=True,
                requires_human_review=False,
                recovery_required=False,
                state_transition="ACQUISITION_MILESTONE_ADVANCED",
            )

        return self._build_resolution(
            outcome=outcome,
            resolution_action="ROUTE_TO_HUMAN_REVIEW",
            resolution_status="REVIEW_REQUIRED",
            next_step=(
                "Route the acquisition outcome to human review before "
                "additional automated execution."
            ),
            automated_resolution_allowed=False,
            requires_human_review=True,
            recovery_required=False,
            state_transition=state_transition or "NO_STATE_CHANGE",
        )

    @staticmethod
    def _build_resolution(
        *,
        outcome: Dict[str, Any],
        resolution_action: str,
        resolution_status: str,
        next_step: str,
        automated_resolution_allowed: bool,
        requires_human_review: bool,
        recovery_required: bool,
        state_transition: str,
    ) -> Dict[str, Any]:
        return {
            "deal_id": outcome.get("deal_id"),
            "resolution_action": resolution_action,
            "resolution_status": resolution_status,
            "source_outcome_status": outcome.get("outcome_status"),
            "source_verification_status": outcome.get(
                "verification_status"
            ),
            "execution_status": outcome.get("execution_status"),
            "original_resolution_action": outcome.get(
                "resolution_action"
            ),
            "state_transition": state_transition,
            "next_step": next_step,
            "automated_resolution_allowed": automated_resolution_allowed,
            "requires_human_review": requires_human_review,
            "recovery_required": recovery_required,
            "status": "ACQUISITION_ACTION_OUTCOME_RESOLVED",
        }


def resolve_acquisition_action_outcomes(
    verification: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convenience function for resolving verified acquisition outcomes.
    """

    resolver = AcquisitionActionOutcomeResolver()
    return resolver.resolve(verification)
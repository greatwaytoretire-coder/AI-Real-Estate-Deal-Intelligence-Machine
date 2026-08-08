from __future__ import annotations

from typing import Any, Dict, List


class AcquisitionActionOutcomeVerifier:
    """
    Verifies whether an authorized acquisition action produced
    the expected execution outcome and state transition.
    """

    EXPECTED_TRANSITIONS = {
        "CONTINUE_CURRENT_MILESTONE": "ACQUISITION_REMAINS_ACTIVE",
        "ADVANCE_ACQUISITION_MILESTONE": "ACQUISITION_MILESTONE_ADVANCED",
        "RESOLVE_BLOCKING_CONDITION": "ACQUISITION_REMAINS_BLOCKED",
        "RECOVER_STALLED_ACQUISITION": "ACQUISITION_REMAINS_RECOVERY_REQUIRED",
        "ROUTE_TO_HUMAN_REVIEW": "ACQUISITION_REMAINS_REVIEW_REQUIRED",
        "UNAUTHORIZED_ACTION": "NO_STATE_CHANGE",
    }

    def verify_action(self, execution: Dict[str, Any]) -> Dict[str, Any]:
        deal_id = execution.get("deal_id")
        action = execution.get("resolution_action")
        execution_status = execution.get("execution_status")
        actual_transition = execution.get("state_transition")
        requires_human_review = execution.get(
            "requires_human_review",
            False,
        )

        expected_transition = self.EXPECTED_TRANSITIONS.get(action)

        if expected_transition is None:
            return {
                "deal_id": deal_id,
                "resolution_action": action,
                "execution_status": execution_status,
                "expected_state_transition": None,
                "actual_state_transition": actual_transition,
                "verification_status": "FAILED",
                "outcome_status": "UNRECOGNIZED_ACTION",
                "state_reconciled": False,
                "requires_human_review": True,
                "recommendation": (
                    "Do not continue execution. "
                    "The acquisition action is not recognized."
                ),
                "status": "ACQUISITION_ACTION_OUTCOME_VERIFIED",
            }

        if execution_status == "REJECTED":
            outcome_status = "REJECTED"
            verification_status = (
                "SUCCESS"
                if actual_transition == expected_transition
                else "STATE_MISMATCH"
            )
        elif execution_status == "HUMAN_ACTION_REQUIRED":
            outcome_status = "DEFERRED_TO_HUMAN"
            verification_status = (
                "SUCCESS"
                if actual_transition == expected_transition
                else "STATE_MISMATCH"
            )
        elif execution_status == "EXECUTED":
            outcome_status = "EXECUTION_SUCCESSFUL"
            verification_status = (
                "SUCCESS"
                if actual_transition == expected_transition
                else "STATE_MISMATCH"
            )
        else:
            outcome_status = "EXECUTION_FAILED"
            verification_status = "FAILED"

        state_reconciled = verification_status == "SUCCESS"

        if verification_status == "SUCCESS":
            recommendation = (
                "Expected and actual acquisition states are reconciled."
            )
        elif verification_status == "STATE_MISMATCH":
            recommendation = (
                "Stop additional automated execution and investigate "
                "the acquisition state mismatch."
            )
        else:
            recommendation = (
                "Investigate the acquisition action outcome before "
                "continuing execution."
            )

        return {
            "deal_id": deal_id,
            "resolution_action": action,
            "execution_status": execution_status,
            "expected_state_transition": expected_transition,
            "actual_state_transition": actual_transition,
            "verification_status": verification_status,
            "outcome_status": outcome_status,
            "state_reconciled": state_reconciled,
            "requires_human_review": (
                requires_human_review
                or verification_status != "SUCCESS"
            ),
            "recommendation": recommendation,
            "status": "ACQUISITION_ACTION_OUTCOME_VERIFIED",
        }

    def verify_executions(
        self,
        executions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        verifications = [
            self.verify_action(execution)
            for execution in executions
        ]

        successful = [
            result
            for result in verifications
            if result["verification_status"] == "SUCCESS"
        ]

        mismatches = [
            result
            for result in verifications
            if result["verification_status"] == "STATE_MISMATCH"
        ]

        failed = [
            result
            for result in verifications
            if result["verification_status"] == "FAILED"
        ]

        human_review = [
            result
            for result in verifications
            if result["requires_human_review"]
        ]

        return {
            "verifications": verifications,
            "successful": successful,
            "mismatches": mismatches,
            "failed": failed,
            "human_review_required": human_review,
            "summary": {
                "total_actions": len(verifications),
                "successful_count": len(successful),
                "mismatch_count": len(mismatches),
                "failed_count": len(failed),
                "human_review_count": len(human_review),
            },
            "status": "ACQUISITION_ACTION_OUTCOME_VERIFICATION_COMPLETE",
        }
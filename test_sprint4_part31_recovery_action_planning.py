from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_recovery_action_planner import (
    AcquisitionRecoveryActionPlanner,
)
from ai_real_estate_deal_intelligence_machine.learning.acquisition_recovery_action_planner_integration import (
    AcquisitionRecoveryActionPlanningIntegration,
)


def build_part30_results():
    return {
        "status": "ACQUISITION_ACTION_OUTCOME_RESOLUTION_COMPLETE",
        "resolutions": [
            {
                "deal_id": "DEAL-001",
                "execution_status": "EXECUTED",
                "source_outcome_status": "EXECUTION_SUCCESSFUL",
                "source_verification_status": "SUCCESS",
                "resolution_action": "CONTINUE_ACQUISITION",
                "resolution_status": "CONTINUED",
                "recovery_required": False,
                "requires_human_review": False,
                "state_transition": "ACQUISITION_REMAINS_ACTIVE",
            },
            {
                "deal_id": "DEAL-002",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "source_outcome_status": "DEFERRED_TO_HUMAN",
                "source_verification_status": "SUCCESS",
                "resolution_action": "MAINTAIN_HUMAN_CONTROL",
                "resolution_status": "DEFERRED",
                "recovery_required": False,
                "requires_human_review": True,
                "state_transition": "ACQUISITION_REMAINS_BLOCKED",
            },
            {
                "deal_id": "DEAL-003",
                "execution_status": "EXECUTED",
                "source_outcome_status": "EXECUTION_SUCCESSFUL",
                "source_verification_status": "SUCCESS",
                "resolution_action": "PROCEED_TO_NEXT_MILESTONE",
                "resolution_status": "ADVANCE_APPROVED",
                "recovery_required": False,
                "requires_human_review": False,
                "state_transition": "ACQUISITION_MILESTONE_ADVANCED",
            },
            {
                "deal_id": "DEAL-004",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "source_outcome_status": "DEFERRED_TO_HUMAN",
                "source_verification_status": "SUCCESS",
                "resolution_action": "MAINTAIN_HUMAN_CONTROL",
                "resolution_status": "DEFERRED",
                "recovery_required": False,
                "requires_human_review": True,
                "state_transition": (
                    "ACQUISITION_REMAINS_RECOVERY_REQUIRED"
                ),
            },
            {
                "deal_id": "DEAL-005",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "source_outcome_status": "DEFERRED_TO_HUMAN",
                "source_verification_status": "SUCCESS",
                "resolution_action": "MAINTAIN_HUMAN_CONTROL",
                "resolution_status": "DEFERRED",
                "recovery_required": False,
                "requires_human_review": True,
                "state_transition": (
                    "ACQUISITION_REMAINS_REVIEW_REQUIRED"
                ),
            },
            {
                "deal_id": "DEAL-006",
                "execution_status": "REJECTED",
                "source_outcome_status": "REJECTED",
                "source_verification_status": "SUCCESS",
                "resolution_action": "PRESERVE_REJECTED_STATE",
                "resolution_status": "REJECTED",
                "recovery_required": False,
                "requires_human_review": True,
                "state_transition": "NO_STATE_CHANGE",
            },
        ],
    }


def main():
    print("=" * 70)
    print("SPRINT 4 PART 31 INTEGRATION TEST")
    print("ACQUISITION RECOVERY ACTION PLANNING")
    print("=" * 70)

    print("\nSTEP 1 - Loading Part 30 Resolution Results")

    part30_results = build_part30_results()
    pprint(part30_results)

    print("\nSTEP 2 - Running Recovery Action Planning")

    integration = AcquisitionRecoveryActionPlanningIntegration()

    result = integration.plan_recovery(part30_results)

    pprint(result)

    assert (
        result["status"]
        == "ACQUISITION_RECOVERY_ACTION_PLANNING_COMPLETE"
    )

    assert result["summary"]["total_outcomes"] == 6
    assert result["summary"]["automatic_plan_count"] == 2
    assert result["summary"]["human_review_count"] == 4
    assert result["summary"]["recovery_required_count"] == 0

    print("\nSTEP 3 - Planning Results")

    for plan in result["plans"]:
        print(
            f"{plan['deal_id']} | "
            f"Source Outcome: {plan['source_outcome_status']} | "
            f"Verification: {plan['source_verification_status']} | "
            f"Recovery Action: {plan['recovery_action']} | "
            f"Planning Status: {plan['planning_status']} | "
            f"Automatic Planning: "
            f"{plan['automated_planning_allowed']} | "
            f"Human Review: "
            f"{plan['requires_human_review']} | "
            f"Recovery Required: "
            f"{plan['recovery_required']}"
        )

    automatic_plans = result["automatic_plans"]

    assert len(automatic_plans) == 2

    assert automatic_plans[0]["deal_id"] == "DEAL-001"
    assert (
        automatic_plans[0]["recovery_action"]
        == "CONTINUE_ACQUISITION"
    )
    assert (
        automatic_plans[0]["execution_authorization_required"]
        is False
    )

    assert automatic_plans[1]["deal_id"] == "DEAL-003"
    assert (
        automatic_plans[1]["recovery_action"]
        == "PROCEED_TO_NEXT_MILESTONE"
    )
    assert (
        automatic_plans[1]["execution_authorization_required"]
        is False
    )

    print("\nSTEP 4 - Human Control Validation")

    human_required = result["human_required"]

    assert len(human_required) == 4

    for plan in human_required:
        assert plan["requires_human_review"] is True

    print("Human control validation successful")

    print("\nSTEP 5 - Rejected Action Validation")

    rejected = next(
        plan
        for plan in result["plans"]
        if plan["deal_id"] == "DEAL-006"
    )

    assert (
        rejected["recovery_action"]
        == "PRESERVE_REJECTED_STATE"
    )
    assert rejected["automated_planning_allowed"] is False
    assert rejected["execution_authorization_required"] is True

    print("Rejected action validation successful")

    print("\nSTEP 6 - Testing State Mismatch Planning")

    mismatch = {
        "deal_id": "DEAL-007",
        "execution_status": "EXECUTED",
        "source_outcome_status": "EXECUTION_SUCCESSFUL",
        "source_verification_status": "STATE_MISMATCH",
        "resolution_action": "INVESTIGATE_STATE_MISMATCH",
        "resolution_status": "ESCALATED",
        "recovery_required": True,
        "requires_human_review": True,
        "state_transition": (
            "ACQUISITION_REMAINS_REVIEW_REQUIRED"
        ),
    }

    mismatch_result = integration.plan_single_recovery(
        mismatch
    )

    pprint(mismatch_result)

    assert (
        mismatch_result["recovery_action"]
        == "INVESTIGATE_STATE_MISMATCH"
    )
    assert mismatch_result["recovery_required"] is True
    assert mismatch_result["requires_human_review"] is True
    assert mismatch_result["execution_authorization_required"] is True

    print("State mismatch planning validation successful")

    print("\nSTEP 7 - Testing Failed Execution Planning")

    failed_execution = {
        "deal_id": "DEAL-008",
        "execution_status": "EXECUTION_FAILED",
        "source_outcome_status": "EXECUTION_FAILED",
        "source_verification_status": "FAILED",
        "resolution_action": "RECOVER_FAILED_EXECUTION",
        "resolution_status": "RECOVERY_REQUIRED",
        "recovery_required": True,
        "requires_human_review": True,
        "state_transition": (
            "ACQUISITION_REMAINS_RECOVERY_REQUIRED"
        ),
    }

    failed_result = integration.plan_single_recovery(
        failed_execution
    )

    pprint(failed_result)

    assert (
        failed_result["recovery_action"]
        == "RECOVER_FAILED_EXECUTION"
    )
    assert failed_result["recovery_required"] is True
    assert failed_result["requires_human_review"] is True
    assert failed_result["execution_authorization_required"] is True

    print("Failed execution planning validation successful")

    print("\nSTEP 8 - Verifying Planning Does Not Execute Actions")

    for plan in result["plans"]:
        assert "execution_result" not in plan
        assert "executed" not in plan
        assert "execution_status" in plan

    print("Execution boundary validation successful")

    print("\nSTEP 9 - Final Validation")

    print("Validation successful")

    print("=" * 70)
    print("SPRINT 4 PART 31 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
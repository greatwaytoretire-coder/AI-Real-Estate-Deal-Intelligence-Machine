from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_action_outcome_resolution import (
    AcquisitionActionOutcomeResolver,
)


def build_part29_verification_results():
    return {
        "status": "ACQUISITION_ACTION_OUTCOME_VERIFICATION_COMPLETE",
        "verifications": [
            {
                "deal_id": "DEAL-001",
                "execution_status": "EXECUTED",
                "outcome_status": "EXECUTION_SUCCESSFUL",
                "verification_status": "SUCCESS",
                "resolution_action": "CONTINUE_CURRENT_MILESTONE",
                "actual_state_transition": "ACQUISITION_REMAINS_ACTIVE",
            },
            {
                "deal_id": "DEAL-002",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "outcome_status": "DEFERRED_TO_HUMAN",
                "verification_status": "SUCCESS",
                "resolution_action": "RESOLVE_BLOCKING_CONDITION",
                "actual_state_transition": "ACQUISITION_REMAINS_BLOCKED",
            },
            {
                "deal_id": "DEAL-003",
                "execution_status": "EXECUTED",
                "outcome_status": "EXECUTION_SUCCESSFUL",
                "verification_status": "SUCCESS",
                "resolution_action": "ADVANCE_ACQUISITION_MILESTONE",
                "actual_state_transition": "ACQUISITION_MILESTONE_ADVANCED",
            },
            {
                "deal_id": "DEAL-004",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "outcome_status": "DEFERRED_TO_HUMAN",
                "verification_status": "SUCCESS",
                "resolution_action": "RECOVER_STALLED_ACQUISITION",
                "actual_state_transition": (
                    "ACQUISITION_REMAINS_RECOVERY_REQUIRED"
                ),
            },
            {
                "deal_id": "DEAL-005",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "outcome_status": "DEFERRED_TO_HUMAN",
                "verification_status": "SUCCESS",
                "resolution_action": "ROUTE_TO_HUMAN_REVIEW",
                "actual_state_transition": (
                    "ACQUISITION_REMAINS_REVIEW_REQUIRED"
                ),
            },
            {
                "deal_id": "DEAL-006",
                "execution_status": "REJECTED",
                "outcome_status": "REJECTED",
                "verification_status": "SUCCESS",
                "resolution_action": "UNAUTHORIZED_ACTION",
                "actual_state_transition": "NO_STATE_CHANGE",
            },
        ],
    }


def build_state_mismatch_case():
    return {
        "status": "ACQUISITION_ACTION_OUTCOME_VERIFICATION_COMPLETE",
        "verifications": [
            {
                "deal_id": "DEAL-007",
                "execution_status": "EXECUTED",
                "outcome_status": "EXECUTION_SUCCESSFUL",
                "verification_status": "STATE_MISMATCH",
                "resolution_action": "ADVANCE_ACQUISITION_MILESTONE",
                "actual_state_transition": "ACQUISITION_REMAINS_ACTIVE",
            }
        ],
    }


def build_failed_execution_case():
    return {
        "status": "ACQUISITION_ACTION_OUTCOME_VERIFICATION_COMPLETE",
        "verifications": [
            {
                "deal_id": "DEAL-008",
                "execution_status": "EXECUTION_FAILED",
                "outcome_status": "EXECUTION_FAILED",
                "verification_status": "FAILED",
                "resolution_action": "CONTINUE_CURRENT_MILESTONE",
                "actual_state_transition": "ACQUISITION_REMAINS_ACTIVE",
            }
        ],
    }


def main():
    print("=" * 70)
    print("SPRINT 4 PART 30 INTEGRATION TEST")
    print("ACQUISITION ACTION OUTCOME RESOLUTION & RECOVERY")
    print("=" * 70)

    resolver = AcquisitionActionOutcomeResolver()

    print("\nSTEP 1 - Loading Part 29 Verification Results")

    verification = build_part29_verification_results()
    pprint(verification)

    print("\nSTEP 2 - Running Outcome Resolution")

    resolution = resolver.resolve(verification)
    pprint(resolution)

    print("\nSTEP 3 - Resolution Results")

    for item in resolution["resolutions"]:
        print(
            f"{item['deal_id']} | "
            f"Source Outcome: {item['source_outcome_status']} | "
            f"Source Verification: {item['source_verification_status']} | "
            f"Resolution: {item['resolution_action']} | "
            f"Status: {item['resolution_status']} | "
            f"Transition: {item['state_transition']} | "
            f"Automatic: {item['automated_resolution_allowed']} | "
            f"Human Review: {item['requires_human_review']} | "
            f"Recovery: {item['recovery_required']}"
        )

    print("\nSTEP 4 - Automatic Resolutions")

    pprint(resolution["automatic_resolutions"])

    assert len(resolution["automatic_resolutions"]) == 2

    automatic_deals = {
        item["deal_id"]
        for item in resolution["automatic_resolutions"]
    }

    assert automatic_deals == {"DEAL-001", "DEAL-003"}

    print("Automatic resolution validation successful")

    print("\nSTEP 5 - Human Required")

    pprint(resolution["human_required"])

    assert len(resolution["human_required"]) == 4

    human_deals = {
        item["deal_id"]
        for item in resolution["human_required"]
    }

    assert human_deals == {
        "DEAL-002",
        "DEAL-004",
        "DEAL-005",
        "DEAL-006",
    }

    print("Human review routing validation successful")

    print("\nSTEP 6 - Recovery Required")

    pprint(resolution["recovery_required"])

    assert len(resolution["recovery_required"]) == 0

    print("Normal recovery validation successful")

    print("\nSTEP 7 - Testing State Mismatch Recovery")

    mismatch_resolution = resolver.resolve(
        build_state_mismatch_case()
    )

    pprint(mismatch_resolution)

    mismatch = mismatch_resolution["resolutions"][0]

    assert mismatch["deal_id"] == "DEAL-007"
    assert (
        mismatch["resolution_action"]
        == "INVESTIGATE_STATE_MISMATCH"
    )
    assert mismatch["resolution_status"] == "ESCALATED"
    assert mismatch["automated_resolution_allowed"] is False
    assert mismatch["requires_human_review"] is True
    assert mismatch["recovery_required"] is True
    assert (
        mismatch["state_transition"]
        == "ACQUISITION_REMAINS_REVIEW_REQUIRED"
    )

    print("State mismatch recovery validation successful")

    print("\nSTEP 8 - Testing Failed Execution Recovery")

    failed_resolution = resolver.resolve(
        build_failed_execution_case()
    )

    pprint(failed_resolution)

    failed = failed_resolution["resolutions"][0]

    assert failed["deal_id"] == "DEAL-008"
    assert (
        failed["resolution_action"]
        == "RECOVER_FAILED_EXECUTION"
    )
    assert failed["resolution_status"] == "RECOVERY_REQUIRED"
    assert failed["automated_resolution_allowed"] is False
    assert failed["requires_human_review"] is True
    assert failed["recovery_required"] is True
    assert (
        failed["state_transition"]
        == "ACQUISITION_REMAINS_RECOVERY_REQUIRED"
    )

    print("Failed execution recovery validation successful")

    print("\nSTEP 9 - Resolution Summary")

    expected_summary = {
        "total_outcomes": 6,
        "automatic_resolution_count": 2,
        "human_review_count": 4,
        "recovery_required_count": 0,
    }

    print(resolution["summary"])

    assert resolution["summary"] == expected_summary

    print("Resolution summary validation successful")

    print("\nSTEP 10 - Final Validation")

    assert resolution["status"] == (
        "ACQUISITION_ACTION_OUTCOME_RESOLUTION_COMPLETE"
    )

    assert resolution["source_status"] == (
        "ACQUISITION_ACTION_OUTCOME_VERIFICATION_COMPLETE"
    )

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 30 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
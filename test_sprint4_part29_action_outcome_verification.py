from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_action_outcome_integration import (
    AcquisitionActionOutcomeIntegration,
)


def build_part28_execution_results():
    return {
        "executions": [
            {
                "deal_id": "DEAL-001",
                "resolution_action": "CONTINUE_CURRENT_MILESTONE",
                "execution_status": "EXECUTED",
                "execution_type": "AUTOMATED_CONTINUATION",
                "state_transition": "ACQUISITION_REMAINS_ACTIVE",
                "requires_human_review": False,
            },
            {
                "deal_id": "DEAL-002",
                "resolution_action": "RESOLVE_BLOCKING_CONDITION",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "execution_type": "HUMAN_CONTROLLED_ACTION",
                "state_transition": "ACQUISITION_REMAINS_BLOCKED",
                "requires_human_review": True,
            },
            {
                "deal_id": "DEAL-003",
                "resolution_action": "ADVANCE_ACQUISITION_MILESTONE",
                "execution_status": "EXECUTED",
                "execution_type": "AUTOMATED_MILESTONE_ADVANCEMENT",
                "state_transition": "ACQUISITION_MILESTONE_ADVANCED",
                "requires_human_review": False,
            },
            {
                "deal_id": "DEAL-004",
                "resolution_action": "RECOVER_STALLED_ACQUISITION",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "execution_type": "HUMAN_CONTROLLED_ACTION",
                "state_transition": "ACQUISITION_REMAINS_RECOVERY_REQUIRED",
                "requires_human_review": True,
            },
            {
                "deal_id": "DEAL-005",
                "resolution_action": "ROUTE_TO_HUMAN_REVIEW",
                "execution_status": "HUMAN_ACTION_REQUIRED",
                "execution_type": "HUMAN_CONTROLLED_ACTION",
                "state_transition": "ACQUISITION_REMAINS_REVIEW_REQUIRED",
                "requires_human_review": True,
            },
            {
                "deal_id": "DEAL-006",
                "resolution_action": "UNAUTHORIZED_ACTION",
                "execution_status": "REJECTED",
                "execution_type": "UNAUTHORIZED_ACTION",
                "state_transition": "NO_STATE_CHANGE",
                "requires_human_review": True,
            },
        ],
        "status": "AUTHORIZED_ACQUISITION_ACTION_INTEGRATION_COMPLETE",
    }


def build_state_mismatch_execution():
    return {
        "executions": [
            {
                "deal_id": "DEAL-007",
                "resolution_action": "ADVANCE_ACQUISITION_MILESTONE",
                "execution_status": "EXECUTED",
                "execution_type": "AUTOMATED_MILESTONE_ADVANCEMENT",
                "state_transition": "ACQUISITION_REMAINS_ACTIVE",
                "requires_human_review": False,
            }
        ],
        "status": "AUTHORIZED_ACQUISITION_ACTION_INTEGRATION_COMPLETE",
    }


def build_failed_execution():
    return {
        "executions": [
            {
                "deal_id": "DEAL-008",
                "resolution_action": "CONTINUE_CURRENT_MILESTONE",
                "execution_status": "EXECUTION_FAILED",
                "execution_type": "AUTOMATED_CONTINUATION",
                "state_transition": "ACQUISITION_REMAINS_ACTIVE",
                "requires_human_review": False,
            }
        ],
        "status": "AUTHORIZED_ACQUISITION_ACTION_INTEGRATION_COMPLETE",
    }


def validate_normal_results(result):
    verification = result["verification"]

    assert result["status"] == (
        "ACQUISITION_ACTION_OUTCOME_INTEGRATION_COMPLETE"
    )

    assert verification["summary"]["total_actions"] == 6
    assert verification["summary"]["successful_count"] == 6
    assert verification["summary"]["mismatch_count"] == 0
    assert verification["summary"]["failed_count"] == 0

    assert len(verification["successful"]) == 6
    assert len(verification["mismatches"]) == 0
    assert len(verification["failed"]) == 0

    return True


def validate_state_mismatch(result):
    verification = result["verification"]

    assert verification["summary"]["total_actions"] == 1
    assert verification["summary"]["successful_count"] == 0
    assert verification["summary"]["mismatch_count"] == 1
    assert verification["summary"]["failed_count"] == 0

    mismatch = verification["mismatches"][0]

    assert mismatch["deal_id"] == "DEAL-007"
    assert mismatch["verification_status"] == "STATE_MISMATCH"
    assert mismatch["state_reconciled"] is False
    assert mismatch["requires_human_review"] is True

    return True


def validate_failed_execution(result):
    verification = result["verification"]

    assert verification["summary"]["total_actions"] == 1
    assert verification["summary"]["successful_count"] == 0
    assert verification["summary"]["mismatch_count"] == 0
    assert verification["summary"]["failed_count"] == 1

    failed = verification["failed"][0]

    assert failed["deal_id"] == "DEAL-008"
    assert failed["verification_status"] == "FAILED"
    assert failed["state_reconciled"] is False
    assert failed["requires_human_review"] is True

    return True


def main():
    print("=" * 70)
    print("SPRINT 4 PART 29 INTEGRATION TEST")
    print("ACQUISITION ACTION OUTCOME & STATE VERIFICATION")
    print("=" * 70)

    integration = AcquisitionActionOutcomeIntegration()

    print("\nSTEP 1 - Loading Part 28 Execution Results")

    source_results = build_part28_execution_results()
    pprint(source_results)

    print("\nSTEP 2 - Running Outcome Verification")

    result = integration.analyze(source_results)
    pprint(result)

    print("\nSTEP 3 - Verification Results")

    for verification in result["verification"]["verifications"]:
        print(
            f"{verification['deal_id']} | "
            f"Action: {verification['resolution_action']} | "
            f"Execution: {verification['execution_status']} | "
            f"Expected: {verification['expected_state_transition']} | "
            f"Actual: {verification['actual_state_transition']} | "
            f"Verification: {verification['verification_status']} | "
            f"Outcome: {verification['outcome_status']} | "
            f"Reconciled: {verification['state_reconciled']} | "
            f"Human Review: {verification['requires_human_review']}"
        )

    print("\nSTEP 4 - Successful Outcomes")

    pprint(result["verification"]["successful"])

    print("\nSTEP 5 - State Mismatches")

    pprint(result["verification"]["mismatches"])

    print("\nSTEP 6 - Failed Outcomes")

    pprint(result["verification"]["failed"])

    print("\nSTEP 7 - Human Review Required")

    pprint(result["verification"]["human_review_required"])

    print("\nSTEP 8 - Verification Summary")

    pprint(result["verification"]["summary"])

    print("\nSTEP 9 - Validation of Normal Execution Results")

    assert validate_normal_results(result)
    print("Normal execution validation successful")

    print("\nSTEP 10 - Testing State Mismatch Detection")

    mismatch_result = integration.analyze(
        build_state_mismatch_execution()
    )

    pprint(mismatch_result)

    assert validate_state_mismatch(mismatch_result)
    print("State mismatch validation successful")

    print("\nSTEP 11 - Testing Failed Execution Detection")

    failed_result = integration.analyze(
        build_failed_execution()
    )

    pprint(failed_result)

    assert validate_failed_execution(failed_result)
    print("Failed execution validation successful")

    print("\nSTEP 12 - Final Validation")

    assert result["verification"]["summary"] == {
        "total_actions": 6,
        "successful_count": 6,
        "mismatch_count": 0,
        "failed_count": 0,
        "human_review_count": 4,
    }

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 29 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
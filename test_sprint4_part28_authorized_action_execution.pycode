from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.authorized_acquisition_action_integration import (
    AuthorizedAcquisitionActionIntegration,
)


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 28 INTEGRATION TEST")
    print("AUTHORIZED ACQUISITION ACTION EXECUTION & STATE TRANSITION")
    print("=" * 70)

    action_execution_results = {
        "executions": [
            {
                "deal_id": "DEAL-001",
                "current_milestone": "SELLER_CONTACT",
                "resolution_action": "CONTINUE_CURRENT_MILESTONE",
                "progress_status": "NORMAL_PROGRESS",
                "automated_execution_allowed": True,
                "requires_human_review": False,
            },
            {
                "deal_id": "DEAL-002",
                "current_milestone": None,
                "resolution_action": "RESOLVE_BLOCKING_CONDITION",
                "progress_status": "BLOCKED",
                "automated_execution_allowed": False,
                "requires_human_review": True,
            },
            {
                "deal_id": "DEAL-003",
                "current_milestone": "PROPERTY_DUE_DILIGENCE",
                "resolution_action": "ADVANCE_ACQUISITION_MILESTONE",
                "progress_status": "READY_TO_ADVANCE",
                "automated_execution_allowed": True,
                "requires_human_review": False,
            },
            {
                "deal_id": "DEAL-004",
                "current_milestone": "NEGOTIATION",
                "resolution_action": "RECOVER_STALLED_ACQUISITION",
                "progress_status": "STALLED",
                "automated_execution_allowed": False,
                "requires_human_review": True,
            },
            {
                "deal_id": "DEAL-005",
                "current_milestone": "PURCHASE_AGREEMENT",
                "resolution_action": "ROUTE_TO_HUMAN_REVIEW",
                "progress_status": "REVIEW_REQUIRED",
                "automated_execution_allowed": False,
                "requires_human_review": True,
            },
            {
                "deal_id": "DEAL-006",
                "current_milestone": "SELLER_CONTACT",
                "resolution_action": "UNAUTHORIZED_ACTION",
                "progress_status": "NORMAL_PROGRESS",
                "automated_execution_allowed": True,
                "requires_human_review": False,
            },
        ],
        "status": "ACQUISITION_ACTION_EXECUTION_INTEGRATION_COMPLETE",
    }

    print("\nSTEP 1 - Loading Part 27 Action Execution Results")
    pprint(action_execution_results)

    integration = AuthorizedAcquisitionActionIntegration()

    print("\nSTEP 2 - Running Authorized Acquisition Action Execution")
    result = integration.run(action_execution_results)
    pprint(result)

    print("\nSTEP 3 - Execution Results")

    for execution in result["executions"]:
        print(
            f"{execution['deal_id']} | "
            f"Action: {execution['resolution_action']} | "
            f"Execution: {execution['execution_type']} | "
            f"Status: {execution['execution_status']} | "
            f"Transition: {execution['state_transition']}"
        )

        if "next_milestone" in execution:
            print(
                f"    Next Milestone: {execution['next_milestone']}"
            )

    print("\nSTEP 4 - Automatic Executions")
    pprint(result["automatic_executions"])

    print("\nSTEP 5 - Human Required")
    pprint(result["human_required"])

    print("\nSTEP 6 - Rejected Actions")
    pprint(result["rejected"])

    print("\nSTEP 7 - Execution Summary")
    pprint(result["summary"])

    print("\nSTEP 8 - Validation")

    assert result["summary"]["total_actions"] == 6
    assert result["summary"]["executed_count"] == 2
    assert result["summary"]["human_action_count"] == 3
    assert result["summary"]["rejected_count"] == 1

    deal_001 = next(
        item for item in result["executions"]
        if item["deal_id"] == "DEAL-001"
    )

    assert deal_001["execution_status"] == "EXECUTED"
    assert deal_001["state_transition"] == "ACQUISITION_REMAINS_ACTIVE"

    deal_003 = next(
        item for item in result["executions"]
        if item["deal_id"] == "DEAL-003"
    )

    assert deal_003["execution_status"] == "EXECUTED"
    assert deal_003["previous_milestone"] == "PROPERTY_DUE_DILIGENCE"
    assert deal_003["next_milestone"] == "NEGOTIATION"
    assert deal_003["state_transition"] == (
        "ACQUISITION_MILESTONE_ADVANCED"
    )

    deal_002 = next(
        item for item in result["executions"]
        if item["deal_id"] == "DEAL-002"
    )

    assert deal_002["execution_status"] == "HUMAN_ACTION_REQUIRED"
    assert deal_002["state_transition"] == (
        "ACQUISITION_REMAINS_BLOCKED"
    )

    deal_004 = next(
        item for item in result["executions"]
        if item["deal_id"] == "DEAL-004"
    )

    assert deal_004["execution_status"] == "HUMAN_ACTION_REQUIRED"
    assert deal_004["state_transition"] == (
        "ACQUISITION_REMAINS_RECOVERY_REQUIRED"
    )

    deal_005 = next(
        item for item in result["executions"]
        if item["deal_id"] == "DEAL-005"
    )

    assert deal_005["execution_status"] == "HUMAN_ACTION_REQUIRED"
    assert deal_005["state_transition"] == (
        "ACQUISITION_REMAINS_REVIEW_REQUIRED"
    )

    deal_006 = next(
        item for item in result["executions"]
        if item["deal_id"] == "DEAL-006"
    )

    assert deal_006["execution_status"] == "REJECTED"
    assert deal_006["state_transition"] == "NO_STATE_CHANGE"

    assert (
        result["status"]
        == "AUTHORIZED_ACQUISITION_ACTION_INTEGRATION_COMPLETE"
    )

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 28 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
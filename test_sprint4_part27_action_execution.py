from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_action_execution_integration import (
    AcquisitionActionExecutionIntegration,
)


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 27 INTEGRATION TEST")
    print("ACQUISITION ACTION EXECUTION & RESOLUTION ORCHESTRATION")
    print("=" * 70)

    resolution_result = {
        "resolution": {
            "resolutions": [
                {
                    "deal_id": "DEAL-001",
                    "current_milestone": "SELLER_CONTACT",
                    "exception_type": None,
                    "progress_status": "NORMAL_PROGRESS",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "resolution_type": "NORMAL_ACQUISITION_CONTINUATION",
                    "resolution_action": "CONTINUE_CURRENT_MILESTONE",
                },
                {
                    "deal_id": "DEAL-002",
                    "current_milestone": None,
                    "exception_type": "ACQUISITION_BLOCKED",
                    "progress_status": "BLOCKED",
                    "execution_state": "ACQUISITION_BLOCKED",
                    "resolution_type": "BLOCKED_ACQUISITION_RESOLUTION",
                    "resolution_action": "RESOLVE_BLOCKING_CONDITION",
                },
                {
                    "deal_id": "DEAL-003",
                    "current_milestone": "PROPERTY_DUE_DILIGENCE",
                    "exception_type": None,
                    "progress_status": "READY_TO_ADVANCE",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "resolution_type": "MILESTONE_ADVANCEMENT",
                    "resolution_action": "ADVANCE_ACQUISITION_MILESTONE",
                },
                {
                    "deal_id": "DEAL-004",
                    "current_milestone": "NEGOTIATION",
                    "exception_type": "MILESTONE_STALLED",
                    "progress_status": "STALLED",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "resolution_type": "STALLED_ACQUISITION_RECOVERY",
                    "resolution_action": "RECOVER_STALLED_ACQUISITION",
                },
                {
                    "deal_id": "DEAL-005",
                    "current_milestone": "PURCHASE_AGREEMENT",
                    "exception_type": "MANUAL_REVIEW_REQUIRED",
                    "progress_status": "REVIEW_REQUIRED",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "resolution_type": "HUMAN_REVIEW",
                    "resolution_action": "ROUTE_TO_HUMAN_REVIEW",
                },
            ]
        },
        "status": "ACQUISITION_EXCEPTION_RESOLUTION_INTEGRATION_COMPLETE",
    }

    integration = AcquisitionActionExecutionIntegration()

    print("\nSTEP 1 - Loading Acquisition Exception Resolution Results")
    pprint(resolution_result)

    print("\nSTEP 2 - Running Acquisition Action Execution")
    result = integration.process_resolution_result(resolution_result)
    pprint(result)

    print("\nSTEP 3 - Execution Results")

    for execution in result["executions"]:
        print(
            f"{execution['deal_id']} | "
            f"Resolution: {execution['resolution_type']} | "
            f"Action: {execution['resolution_action']} | "
            f"Execution: {execution['execution_type']} | "
            f"Status: {execution['execution_status']} | "
            f"Automatic: {execution['automated_execution_allowed']} | "
            f"Human Review: {execution['requires_human_review']}"
        )

    print("\nSTEP 4 - Automatic Execution Actions")
    pprint(integration.get_automatic_execution_actions(result))

    print("\nSTEP 5 - Human Review Actions")
    pprint(integration.get_human_review_actions(result))

    print("\nSTEP 6 - Execution Summary")
    pprint(integration.get_execution_summary(result))

    print("\nSTEP 7 - Validation")

    executions = result["executions"]
    automatic = integration.get_automatic_execution_actions(result)
    human_review = integration.get_human_review_actions(result)

    assert len(executions) == 5
    assert len(automatic) == 2
    assert len(human_review) == 3

    execution_by_deal = {
        execution["deal_id"]: execution
        for execution in executions
    }

    # DEAL-001: normal continuation may execute automatically.
    deal_001 = execution_by_deal["DEAL-001"]

    assert (
        deal_001["resolution_action"]
        == "CONTINUE_CURRENT_MILESTONE"
    )
    assert deal_001["automated_execution_allowed"] is True
    assert deal_001["requires_human_review"] is False
    assert deal_001["execution_status"] == "READY_FOR_EXECUTION"

    # DEAL-002: blocked acquisition must never execute automatically.
    deal_002 = execution_by_deal["DEAL-002"]

    assert (
        deal_002["resolution_action"]
        == "RESOLVE_BLOCKING_CONDITION"
    )
    assert deal_002["automated_execution_allowed"] is False
    assert deal_002["requires_human_review"] is True
    assert deal_002["execution_status"] == "HUMAN_ACTION_REQUIRED"

    # DEAL-003: milestone advancement may execute automatically.
    deal_003 = execution_by_deal["DEAL-003"]

    assert (
        deal_003["resolution_action"]
        == "ADVANCE_ACQUISITION_MILESTONE"
    )
    assert deal_003["automated_execution_allowed"] is True
    assert deal_003["requires_human_review"] is False
    assert deal_003["execution_status"] == "READY_FOR_EXECUTION"

    # DEAL-004: stalled acquisition requires human intervention.
    deal_004 = execution_by_deal["DEAL-004"]

    assert (
        deal_004["resolution_action"]
        == "RECOVER_STALLED_ACQUISITION"
    )
    assert deal_004["automated_execution_allowed"] is False
    assert deal_004["requires_human_review"] is True
    assert deal_004["execution_status"] == "HUMAN_ACTION_REQUIRED"

    # DEAL-005: explicit human review must remain human-controlled.
    deal_005 = execution_by_deal["DEAL-005"]

    assert (
        deal_005["resolution_action"]
        == "ROUTE_TO_HUMAN_REVIEW"
    )
    assert deal_005["automated_execution_allowed"] is False
    assert deal_005["requires_human_review"] is True
    assert deal_005["execution_status"] == "HUMAN_REVIEW_REQUIRED"

    # Safety validation: no human-review action may be automatic.
    for execution in executions:
        if execution["requires_human_review"]:
            assert execution["automated_execution_allowed"] is False

    # Safety validation: every automatic action must explicitly permit
    # automation and explicitly not require human review.
    for execution in automatic:
        assert execution["automated_execution_allowed"] is True
        assert execution["requires_human_review"] is False

    assert result["summary"]["total_executions"] == 5
    assert result["summary"]["automatic_execution_count"] == 2
    assert result["summary"]["human_review_count"] == 3
    assert result["summary"]["rejected_count"] == 0

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 27 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
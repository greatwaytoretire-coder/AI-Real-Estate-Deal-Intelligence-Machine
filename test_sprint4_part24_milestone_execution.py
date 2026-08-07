from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_milestone_execution_integration import (
    AcquisitionMilestoneExecutionIntegration,
)


def build_milestone_plan() -> dict:
    return {
        "deal_id": "DEAL-001",
        "execution_state": "ACQUISITION_ACTIVE",
        "milestone_count": 6,
        "current_milestone": "EXECUTION_INITIATED",
        "next_milestone": "SELLER_CONTACT",
        "completed_count": 0,
        "pending_count": 5,
        "milestones": [
            {
                "milestone": "EXECUTION_INITIATED",
                "sequence": 1,
                "description": "Acquisition execution has been initiated.",
                "status": "CURRENT",
            },
            {
                "milestone": "SELLER_CONTACT",
                "sequence": 2,
                "description": "Seller communication and initial acquisition contact completed.",
                "status": "PENDING",
            },
            {
                "milestone": "PROPERTY_DUE_DILIGENCE",
                "sequence": 3,
                "description": "Property and ownership due diligence completed.",
                "status": "PENDING",
            },
            {
                "milestone": "NEGOTIATION",
                "sequence": 4,
                "description": "Acquisition negotiation completed.",
                "status": "PENDING",
            },
            {
                "milestone": "PURCHASE_AGREEMENT",
                "sequence": 5,
                "description": "Purchase agreement prepared and ready for execution.",
                "status": "PENDING",
            },
            {
                "milestone": "ACQUISITION_COMPLETED",
                "sequence": 6,
                "description": "Acquisition has been completed.",
                "status": "PENDING",
            },
        ],
        "status": "ACQUISITION_MILESTONE_PLAN_CREATED",
    }


def validate_result(result: dict) -> None:
    assert result["total_acquisitions"] == 1

    assert len(result["execution_results"]) == 1
    assert len(result["active_acquisitions"]) == 1
    assert result["active_count"] == 1
    assert result["completed_count"] == 0

    execution = result["execution_results"][0]

    assert execution["deal_id"] == "DEAL-001"
    assert execution["execution_state"] == "ACQUISITION_ACTIVE"

    assert execution["completed_milestone"] == "EXECUTION_INITIATED"
    assert execution["current_milestone"] == "SELLER_CONTACT"
    assert execution["next_milestone"] == "SELLER_CONTACT"

    assert execution["completed_count"] == 1
    assert execution["pending_count"] == 4
    assert execution["milestone_count"] == 6

    assert execution["execution_status"] == "MILESTONE_ADVANCED"
    assert execution["status"] == "ACQUISITION_MILESTONE_EXECUTED"

    milestones = execution["milestones"]

    assert milestones[0]["status"] == "COMPLETED"
    assert milestones[1]["status"] == "CURRENT"

    for milestone in milestones[2:]:
        assert milestone["status"] == "PENDING"


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 24 INTEGRATION TEST")
    print("ACQUISITION MILESTONE EXECUTION INTELLIGENCE")
    print("=" * 70)

    print("\nSTEP 1 - Loading Acquisition Milestone Plan")

    milestone_plan = build_milestone_plan()
    pprint(milestone_plan)

    print("\nSTEP 2 - Running Acquisition Milestone Execution")

    integration = AcquisitionMilestoneExecutionIntegration()
    result = integration.evaluate([milestone_plan])

    pprint(result)

    print("\nSTEP 3 - Executed Acquisition Milestones")

    for execution in result["execution_results"]:
        print(
            f"{execution['deal_id']} | "
            f"Completed: {execution['completed_milestone']} | "
            f"Current: {execution['current_milestone']} | "
            f"Next: {execution['next_milestone']} | "
            f"State: {execution['execution_state']}"
        )

    print("\nSTEP 4 - Milestone Status")

    execution = result["execution_results"][0]

    for milestone in execution["milestones"]:
        print(
            f"{milestone['sequence']}. "
            f"{milestone['milestone']} | "
            f"Status: {milestone['status']}"
        )

    print("\nSTEP 5 - Validation")

    validate_result(result)

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 24 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
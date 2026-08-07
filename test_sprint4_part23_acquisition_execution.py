from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_execution_integration import (
    AcquisitionExecutionIntegration,
)


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 23 INTEGRATION TEST")
    print("ACQUISITION EXECUTION & MILESTONE INTELLIGENCE")
    print("=" * 70)

    print("\nSTEP 1 - Loading Decision Execution Results")

    execution_decisions = [
        {
            "deal_id": "DEAL-001",
            "enforcement_decision": "APPROVE",
            "execution_action": "EXECUTE_ACQUISITION",
            "execution_status": "READY_FOR_EXECUTION",
            "next_step": "Proceed to acquisition execution workflow.",
            "original_action": "PROCEED_WITH_DEAL",
            "recommendation": "PURSUE",
            "risk_level": "LOW",
            "status": "DECISION_EXECUTION_PLAN_GENERATED",
        },
        {
            "deal_id": "DEAL-002",
            "enforcement_decision": "REJECT",
            "execution_action": "DO_NOT_EXECUTE",
            "execution_status": "EXECUTION_BLOCKED",
            "next_step": (
                "Do not execute acquisition; retain outcome for learning."
            ),
            "original_action": "DO_NOT_PROCEED",
            "recommendation": "PASS",
            "risk_level": "MEDIUM",
            "status": "DECISION_EXECUTION_PLAN_GENERATED",
        },
        {
            "deal_id": "DEAL-003",
            "enforcement_decision": "REJECT",
            "execution_action": "DO_NOT_EXECUTE",
            "execution_status": "EXECUTION_BLOCKED",
            "next_step": (
                "Do not execute acquisition; retain outcome for learning."
            ),
            "original_action": "DO_NOT_PROCEED",
            "recommendation": "PASS",
            "risk_level": "HIGH",
            "status": "DECISION_EXECUTION_PLAN_GENERATED",
        },
    ]

    pprint(execution_decisions)

    print("\nSTEP 2 - Running Acquisition Execution Integration")

    integration = AcquisitionExecutionIntegration()
    result = integration.evaluate(execution_decisions)

    pprint(result)

    print("\nSTEP 3 - Active Acquisition Executions")

    active_acquisitions = result.get("active_acquisitions", [])

    pprint(active_acquisitions)

    print("\nSTEP 4 - Acquisition Milestone Plans")

    milestones = result.get("milestones", {})
    milestone_plans = milestones.get("milestone_plans", [])

    pprint(milestone_plans)

    print("\nSTEP 5 - Blocked Acquisitions")

    blocked_acquisitions = result.get("blocked_acquisitions", [])

    pprint(blocked_acquisitions)

    print("\nSTEP 6 - Validation")

    assert result["status"] == (
        "ACQUISITION_EXECUTION_INTEGRATION_COMPLETE"
    )

    assert len(active_acquisitions) == 1

    assert active_acquisitions[0]["deal_id"] == "DEAL-001"

    assert len(blocked_acquisitions) == 2

    assert blocked_acquisitions[0]["deal_id"] == "DEAL-002"
    assert blocked_acquisitions[1]["deal_id"] == "DEAL-003"

    assert milestones["status"] == (
        "ACQUISITION_MILESTONES_GENERATED"
    )

    assert len(milestone_plans) == 1

    milestone_plan = milestone_plans[0]

    assert milestone_plan["deal_id"] == "DEAL-001"

    assert milestone_plan["current_milestone"] == (
        "EXECUTION_INITIATED"
    )

    assert milestone_plan["milestone_count"] == 6

    assert milestone_plan["completed_count"] == 0

    assert milestone_plan["pending_count"] == 5

    assert milestone_plan["next_milestone"] == (
        "SELLER_CONTACT"
    )

    assert milestone_plan["status"] == (
        "ACQUISITION_MILESTONE_PLAN_CREATED"
    )

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 23 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
    
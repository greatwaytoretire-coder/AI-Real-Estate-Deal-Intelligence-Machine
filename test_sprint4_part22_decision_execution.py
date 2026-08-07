from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.decision_execution_integration import (
    DecisionExecutionIntegration,
)


def build_policy_enforcement_results():
    return {
        "total_deals": 3,
        "enforced_decisions": [
            {
                "deal_id": "DEAL-001",
                "enforcement_decision": "APPROVE",
                "action": "PROCEED_WITH_DEAL",
                "recommendation": "PURSUE",
                "recommendation_score": 81.6,
                "original_confidence_score": 91.1,
                "adjusted_confidence_score": 91.1,
                "confidence_adjustment": 0.0,
                "risk_level": "LOW",
                "policy_action": "MAINTAIN_DEAL_SELECTION",
                "policy_version": "1.0",
                "threshold_direction": "MAINTAIN",
                "status": "DECISION_POLICY_ENFORCED",
            },
            {
                "deal_id": "DEAL-002",
                "enforcement_decision": "REJECT",
                "action": "DO_NOT_PROCEED",
                "recommendation": "PASS",
                "recommendation_score": 52.1,
                "original_confidence_score": 56.55,
                "adjusted_confidence_score": 56.55,
                "confidence_adjustment": 0.0,
                "risk_level": "MEDIUM",
                "policy_action": "MAINTAIN_DEAL_SELECTION",
                "policy_version": "1.0",
                "threshold_direction": "MAINTAIN",
                "status": "DECISION_POLICY_ENFORCED",
            },
            {
                "deal_id": "DEAL-003",
                "enforcement_decision": "REJECT",
                "action": "DO_NOT_PROCEED",
                "recommendation": "PASS",
                "recommendation_score": 9.5,
                "original_confidence_score": 8.75,
                "adjusted_confidence_score": 8.75,
                "confidence_adjustment": 0.0,
                "risk_level": "HIGH",
                "policy_action": "MAINTAIN_DEAL_SELECTION",
                "policy_version": "1.0",
                "threshold_direction": "MAINTAIN",
                "status": "DECISION_POLICY_ENFORCED",
            },
        ],
        "approved_count": 1,
        "rejected_count": 2,
        "review_count": 0,
        "review_required": [],
        "status": "POLICY_ENFORCEMENT_COMPLETE",
    }


def main():
    print("=" * 70)
    print("SPRINT 4 PART 22 INTEGRATION TEST")
    print("DECISION EXECUTION INTELLIGENCE")
    print("=" * 70)

    print("\nSTEP 1 - Loading Policy Enforcement Results")

    enforcement_results = build_policy_enforcement_results()

    pprint(enforcement_results["enforced_decisions"])

    print("\nSTEP 2 - Running Decision Execution Integration")

    integration = DecisionExecutionIntegration()

    result = integration.evaluate(enforcement_results)

    pprint(result)

    print("\nSTEP 3 - Executable Acquisition Decisions")

    pprint(result["executable_deals"])

    print("\nSTEP 4 - Human Review Decisions")

    pprint(result["review_required"])

    print("\nSTEP 5 - Blocked Acquisition Decisions")

    pprint(result["blocked_deals"])

    print("\nSTEP 6 - Validation")

    assert result["status"] == (
        "DECISION_EXECUTION_INTEGRATION_COMPLETE"
    )

    execution = result["execution"]

    assert execution["total_deals"] == 3

    assert execution["executable_count"] == 1

    assert execution["review_count"] == 0

    assert execution["blocked_count"] == 2

    assert len(result["executable_deals"]) == 1

    assert len(result["review_required"]) == 0

    assert len(result["blocked_deals"]) == 2

    executable = result["executable_deals"][0]

    assert executable["deal_id"] == "DEAL-001"

    assert executable["execution_action"] == (
        "EXECUTE_ACQUISITION"
    )

    assert executable["execution_status"] == (
        "READY_FOR_EXECUTION"
    )

    assert executable["enforcement_decision"] == "APPROVE"

    blocked_ids = {
        deal["deal_id"]
        for deal in result["blocked_deals"]
    }

    assert blocked_ids == {
        "DEAL-002",
        "DEAL-003",
    }

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 22 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.policy_enforcement_integration import (
    PolicyEnforcementIntegration,
)


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 21 INTEGRATION TEST")
    print("DECISION POLICY ENFORCEMENT INTELLIGENCE")
    print("=" * 70)

    policy = {
        "policy_version": "1.0",
        "optimization": "MAINTAIN_DECISION_THRESHOLDS",
        "success_rate": 66.67,
        "signal_strength": "MEDIUM",
        "confidence_adjustment": 0.0,
        "policy_action": "MAINTAIN_DEAL_SELECTION",
        "threshold_direction": "MAINTAIN",
        "recommendation": (
            "Maintain current decision thresholds because "
            "historical performance supports the existing "
            "decision behavior."
        ),
        "status": "ADAPTIVE_DECISION_POLICY_GENERATED",
    }

    deals = [
        {
            "deal_id": "DEAL-001",
            "recommendation": "PURSUE",
            "recommendation_score": 81.6,
            "confidence_score": 91.1,
            "risk_level": "LOW",
        },
        {
            "deal_id": "DEAL-002",
            "recommendation": "PASS",
            "recommendation_score": 52.1,
            "confidence_score": 56.55,
            "risk_level": "MEDIUM",
        },
        {
            "deal_id": "DEAL-003",
            "recommendation": "PASS",
            "recommendation_score": 9.5,
            "confidence_score": 8.75,
            "risk_level": "HIGH",
        },
    ]

    print()
    print("STEP 1 - Loading Adaptive Decision Policy")
    pprint(policy)

    print()
    print("STEP 2 - Loading Deal Recommendations")
    pprint(deals)

    print()
    print("STEP 3 - Running Decision Policy Enforcement")

    integration = PolicyEnforcementIntegration()

    result = integration.evaluate(
        deals=deals,
        policy=policy,
    )

    pprint(result)

    print()
    print("STEP 4 - Enforcement Results")

    for decision in result["enforced_decisions"]:
        print(
            f"{decision['deal_id']} | "
            f"Decision: {decision['enforcement_decision']} | "
            f"Action: {decision['action']} | "
            f"Recommendation Score: "
            f"{decision['recommendation_score']} | "
            f"Confidence: "
            f"{decision['adjusted_confidence_score']}"
        )

    print()
    print("STEP 5 - Policy Enforcement Summary")

    print(
        f"Approved Deals: {result['approved_count']}"
    )

    print(
        f"Human Review Required: {result['review_count']}"
    )

    print(
        f"Rejected Deals: {result['rejected_count']}"
    )

    print()
    print("STEP 6 - Validation")

    assert result["total_deals"] == 3

    assert result["approved_count"] == 1

    assert result["review_count"] == 0

    assert result["rejected_count"] == 2

    assert (
        result["approved_deals"][0]["deal_id"]
        == "DEAL-001"
    )

    assert (
        result["approved_deals"][0]["enforcement_decision"]
        == "APPROVE"
    )

    assert (
        result["approved_deals"][0]["action"]
        == "PROCEED_WITH_DEAL"
    )

    assert (
        result["rejected_deals"][0]["enforcement_decision"]
        == "REJECT"
    )

    assert result["status"] == "POLICY_ENFORCEMENT_COMPLETE"

    print("Validation successful")

    print()
    print("=" * 70)
    print("SPRINT 4 PART 21 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
from __future__ import annotations

from ai_real_estate_deal_intelligence_machine.learning.decision_policy_integration import (
    DecisionPolicyIntegration,
)


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 20 INTEGRATION TEST")
    print("ADAPTIVE DECISION POLICY INTELLIGENCE")
    print("=" * 70)

    print()
    print("STEP 1 - Loading Adaptive Optimization")

    optimization = {
        "success_rate": 66.67,
        "signal_strength": "MEDIUM",
        "source_adjustment": "REVIEW_DECISION_SIGNALS",
        "optimization": "MAINTAIN_DECISION_THRESHOLDS",
        "confidence_adjustment": 0,
        "status": "ADAPTIVE_OPTIMIZATION_GENERATED",
    }

    print(optimization)

    print()
    print("STEP 2 - Running Decision Policy Integration")

    engine = DecisionPolicyIntegration()
    result = engine.evaluate(optimization)

    print(result)

    print()
    print("STEP 3 - Generated Decision Policy")

    policy = result["policy"]

    print(
        f"Policy Action: {policy['policy_action']}"
    )
    print(
        f"Threshold Direction: {policy['threshold_direction']}"
    )
    print(
        f"Success Rate: {policy['success_rate']}"
    )
    print(
        f"Signal Strength: {policy['signal_strength']}"
    )
    print(
        f"Confidence Adjustment: {policy['confidence_adjustment']}"
    )
    print(
        f"Recommendation: {policy['recommendation']}"
    )

    print()
    print("STEP 4 - Validation")

    assert result["status"] == "DECISION_POLICY_INTEGRATION_COMPLETE"

    assert policy["policy_version"] == "1.0"

    assert (
        policy["optimization"]
        == "MAINTAIN_DECISION_THRESHOLDS"
    )

    assert (
        policy["policy_action"]
        == "MAINTAIN_DEAL_SELECTION"
    )

    assert (
        policy["threshold_direction"]
        == "MAINTAIN"
    )

    assert policy["success_rate"] == 66.67

    assert policy["signal_strength"] == "MEDIUM"

    assert policy["confidence_adjustment"] == 0.0

    assert (
        policy["status"]
        == "ADAPTIVE_DECISION_POLICY_GENERATED"
    )

    print("Validation successful")

    print()
    print("=" * 70)
    print("SPRINT 4 PART 20 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
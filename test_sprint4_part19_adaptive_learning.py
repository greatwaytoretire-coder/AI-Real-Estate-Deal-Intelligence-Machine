"""
Sprint 4 Part 19 Integration Test
Adaptive Decision Learning

Validates:

- Adaptive decision optimization
- Decision adjustment generation
- Learning-to-decision feedback integration
"""


from ai_real_estate_deal_intelligence_machine.learning.adaptive_learning_integration import (
    AdaptiveLearningIntegration,
)


def main():

    print("=" * 70)
    print("SPRINT 4 PART 19 INTEGRATION TEST")
    print("ADAPTIVE DECISION LEARNING")
    print("=" * 70)

    print("\nSTEP 1 - Loading Outcome Learning Signal")

    learning_signal = {
        "success_rate": 66.67,
        "adjustment": "REVIEW_DECISION_SIGNALS",
        "signal_strength": "MEDIUM",
        "status": "LEARNING_SIGNAL_GENERATED",
    }

    print(learning_signal)

    print("\nSTEP 2 - Running Adaptive Learning Integration")

    engine = AdaptiveLearningIntegration()

    result = engine.optimize(
        learning_signal
    )

    print(result)

    print("\nSTEP 3 - Adaptive Optimization")

    print(
        result["optimization"]
    )

    print("\nSTEP 4 - Decision Adjustment")

    print(
        result["adjustment"]
    )

    print("\nSTEP 5 - Validation")

    assert (
        result["status"]
        == "ADAPTIVE_LEARNING_COMPLETE"
    )

    assert (
        result["optimization"]["status"]
        == "ADAPTIVE_OPTIMIZATION_GENERATED"
    )

    assert (
        result["adjustment"]["status"]
        == "DECISION_ADJUSTMENT_GENERATED"
    )

    assert (
        result["optimization"]["success_rate"]
        == 66.67
    )

    assert (
        result["optimization"]["confidence_adjustment"]
        == 0
    )

    assert (
        result["adjustment"]["adjustment_action"]
        == "MAINTAIN_CURRENT_BEHAVIOR"
    )

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 19 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
"""
Sprint 4 Part 19
Decision Adjustment Engine

Converts adaptive optimization signals into practical
decision-making adjustments.
"""


class DecisionAdjustmentEngine:
    """Generates decision adjustments from optimization results."""

    def adjust(self, optimization):
        confidence_adjustment = float(
            optimization.get("confidence_adjustment", 0)
        )

        optimization_type = optimization.get(
            "optimization",
            "MAINTAIN_DECISION_THRESHOLDS",
        )

        if confidence_adjustment > 0:
            adjustment_action = "INCREASE_PURSUIT_CONFIDENCE"
            recommendation = (
                "Strong historical performance supports "
                "greater confidence in future opportunities."
            )

        elif confidence_adjustment < 0:
            adjustment_action = "INCREASE_RISK_CAUTION"
            recommendation = (
                "Historical performance indicates that "
                "future opportunities should receive additional scrutiny."
            )

        else:
            adjustment_action = "MAINTAIN_CURRENT_BEHAVIOR"
            recommendation = (
                "Historical performance supports maintaining "
                "current decision thresholds."
            )

        return {
            "optimization": optimization_type,
            "confidence_adjustment": confidence_adjustment,
            "adjustment_action": adjustment_action,
            "recommendation": recommendation,
            "status": "DECISION_ADJUSTMENT_GENERATED",
        }
"""
Sprint 4 Part 19
Adaptive Decision Optimizer

Uses historical learning signals to determine how future
deal decisions should be adjusted.
"""


class AdaptiveDecisionOptimizer:
    """Determines adaptive adjustments from learning signals."""

    def optimize(self, learning_signal):
        success_rate = float(
            learning_signal.get("success_rate", 0)
        )

        signal_strength = learning_signal.get(
            "signal_strength",
            "LOW",
        )

        adjustment = learning_signal.get(
            "adjustment",
            "NO_ADJUSTMENT",
        )

        if success_rate >= 80:
            optimization = "INCREASE_DECISION_CONFIDENCE"
            confidence_adjustment = 5
        elif success_rate >= 65:
            optimization = "MAINTAIN_DECISION_THRESHOLDS"
            confidence_adjustment = 0
        elif success_rate >= 50:
            optimization = "REVIEW_DECISION_SIGNALS"
            confidence_adjustment = -5
        else:
            optimization = "INCREASE_DECISION_CAUTION"
            confidence_adjustment = -10

        return {
            "success_rate": success_rate,
            "signal_strength": signal_strength,
            "source_adjustment": adjustment,
            "optimization": optimization,
            "confidence_adjustment": confidence_adjustment,
            "status": "ADAPTIVE_OPTIMIZATION_GENERATED",
        }
"""
Sprint 4 Part 19
Adaptive Learning Integration

Connects outcome-learning signals to adaptive decision
optimization and future decision adjustments.
"""

from ai_real_estate_deal_intelligence_machine.learning.adaptive_decision_optimizer import (
    AdaptiveDecisionOptimizer,
)

from ai_real_estate_deal_intelligence_machine.learning.decision_adjustment_engine import (
    DecisionAdjustmentEngine,
)


class AdaptiveLearningIntegration:
    """Integrates learning signals into adaptive decision behavior."""

    def __init__(self):
        self.optimizer = AdaptiveDecisionOptimizer()
        self.adjustment_engine = DecisionAdjustmentEngine()

    def optimize(self, learning_signal):
        optimization = self.optimizer.optimize(
            learning_signal
        )

        adjustment = self.adjustment_engine.adjust(
            optimization
        )

        return {
            "learning_signal": learning_signal,
            "optimization": optimization,
            "adjustment": adjustment,
            "status": "ADAPTIVE_LEARNING_COMPLETE",
        }
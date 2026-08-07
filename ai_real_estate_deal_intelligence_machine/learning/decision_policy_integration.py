from __future__ import annotations

from typing import Any, Dict

from .adaptive_decision_policy_engine import AdaptiveDecisionPolicyEngine


class DecisionPolicyIntegration:
    """
    Integrates adaptive optimization results with the adaptive decision
    policy engine.
    """

    def __init__(self) -> None:
        self.policy_engine = AdaptiveDecisionPolicyEngine()

    def evaluate(self, optimization: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(optimization, dict):
            raise TypeError("optimization must be a dictionary")

        policy = self.policy_engine.generate_policy(optimization)

        return {
            "optimization": optimization,
            "policy": policy,
            "status": "DECISION_POLICY_INTEGRATION_COMPLETE",
        }
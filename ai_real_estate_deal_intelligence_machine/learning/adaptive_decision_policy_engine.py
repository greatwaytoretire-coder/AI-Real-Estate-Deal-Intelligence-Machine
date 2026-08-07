from __future__ import annotations

from typing import Any, Dict


class AdaptiveDecisionPolicyEngine:
    """
    Converts adaptive-learning optimization results into an explicit
    decision policy that can be consumed by downstream deal intelligence.

    This engine is intentionally deterministic and dependency-free.
    """

    def __init__(self) -> None:
        self.policy_version = "1.0"

    def generate_policy(self, optimization: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(optimization, dict):
            raise TypeError("optimization must be a dictionary")

        optimization_name = str(
            optimization.get("optimization", "MAINTAIN_DECISION_THRESHOLDS")
        ).upper()

        confidence_adjustment = float(
            optimization.get("confidence_adjustment", 0.0)
        )

        success_rate = float(
            optimization.get("success_rate", 0.0)
        )

        signal_strength = str(
            optimization.get("signal_strength", "LOW")
        ).upper()

        if optimization_name == "INCREASE_DECISION_THRESHOLDS":
            policy_action = "TIGHTEN_DEAL_SELECTION"
            threshold_direction = "INCREASE"
            recommendation = (
                "Increase decision thresholds because historical performance "
                "indicates that stronger deal-selection criteria are warranted."
            )

        elif optimization_name == "DECREASE_DECISION_THRESHOLDS":
            policy_action = "EXPAND_DEAL_SELECTION"
            threshold_direction = "DECREASE"
            recommendation = (
                "Decrease decision thresholds because historical performance "
                "supports evaluating a broader set of opportunities."
            )

        else:
            policy_action = "MAINTAIN_DEAL_SELECTION"
            threshold_direction = "MAINTAIN"
            recommendation = (
                "Maintain current decision thresholds because historical "
                "performance supports the existing decision behavior."
            )

        policy = {
            "policy_version": self.policy_version,
            "optimization": optimization_name,
            "success_rate": success_rate,
            "signal_strength": signal_strength,
            "confidence_adjustment": confidence_adjustment,
            "policy_action": policy_action,
            "threshold_direction": threshold_direction,
            "recommendation": recommendation,
            "status": "ADAPTIVE_DECISION_POLICY_GENERATED",
        }

        return policy
    
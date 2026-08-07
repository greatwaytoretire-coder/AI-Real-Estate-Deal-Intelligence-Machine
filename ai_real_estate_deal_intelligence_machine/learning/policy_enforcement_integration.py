from __future__ import annotations

from typing import Any, Dict, List

from .decision_policy_enforcement_engine import (
    DecisionPolicyEnforcementEngine,
)


class PolicyEnforcementIntegration:
    """
    Integrates adaptive decision policy with deal-level enforcement.

    This layer applies one generated policy to a collection of deal
    recommendations and identifies which deals may proceed, require
    review, or should be rejected.
    """

    def __init__(
        self,
        enforcement_engine: DecisionPolicyEnforcementEngine | None = None,
    ) -> None:
        self.enforcement_engine = (
            enforcement_engine
            or DecisionPolicyEnforcementEngine()
        )

    def evaluate(
        self,
        deals: List[Dict[str, Any]],
        policy: Dict[str, Any],
    ) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []

        for deal in deals:
            result = self.enforcement_engine.enforce(
                deal=deal,
                policy=policy,
            )
            results.append(result)

        approved = [
            result
            for result in results
            if result["enforcement_decision"] == "APPROVE"
        ]

        review_required = [
            result
            for result in results
            if result["enforcement_decision"] == "REVIEW"
        ]

        rejected = [
            result
            for result in results
            if result["enforcement_decision"] == "REJECT"
        ]

        return {
            "total_deals": len(results),
            "enforced_decisions": results,
            "approved_deals": approved,
            "review_required": review_required,
            "rejected_deals": rejected,
            "approved_count": len(approved),
            "review_count": len(review_required),
            "rejected_count": len(rejected),
            "status": "POLICY_ENFORCEMENT_COMPLETE",
        }
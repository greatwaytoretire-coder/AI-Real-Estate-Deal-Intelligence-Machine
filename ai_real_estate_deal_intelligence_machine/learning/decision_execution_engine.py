from __future__ import annotations

from typing import Any, Dict, List


class DecisionExecutionEngine:
    """
    Converts policy enforcement results into executable acquisition actions.

    This layer does not perform external side effects. It produces a
    deterministic execution plan that downstream workflow automation
    can consume.
    """

    def evaluate(
        self,
        enforcement_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not isinstance(enforcement_results, dict):
            raise TypeError("enforcement_results must be a dictionary")

        enforced_decisions = enforcement_results.get(
            "enforced_decisions",
            [],
        )

        if not isinstance(enforced_decisions, list):
            raise TypeError("enforced_decisions must be a list")

        execution_plans: List[Dict[str, Any]] = []

        for decision in enforced_decisions:
            if not isinstance(decision, dict):
                continue

            deal_id = decision.get("deal_id")
            enforcement_decision = decision.get(
                "enforcement_decision"
            )
            action = decision.get("action")
            recommendation = decision.get("recommendation")
            risk_level = decision.get("risk_level")

            if enforcement_decision == "APPROVE":
                execution_action = "EXECUTE_ACQUISITION"
                execution_status = "READY_FOR_EXECUTION"
                next_step = (
                    "Proceed to acquisition execution workflow."
                )

            elif enforcement_decision == "REVIEW":
                execution_action = "REQUIRE_HUMAN_REVIEW"
                execution_status = "AWAITING_HUMAN_REVIEW"
                next_step = (
                    "Pause execution and obtain human approval."
                )

            else:
                execution_action = "DO_NOT_EXECUTE"
                execution_status = "EXECUTION_BLOCKED"
                next_step = (
                    "Do not execute acquisition; retain outcome for learning."
                )

            execution_plans.append(
                {
                    "deal_id": deal_id,
                    "enforcement_decision": enforcement_decision,
                    "original_action": action,
                    "recommendation": recommendation,
                    "risk_level": risk_level,
                    "execution_action": execution_action,
                    "execution_status": execution_status,
                    "next_step": next_step,
                    "status": "DECISION_EXECUTION_PLAN_GENERATED",
                }
            )

        executable_deals = [
            plan
            for plan in execution_plans
            if plan["execution_action"] == "EXECUTE_ACQUISITION"
        ]

        review_required = [
            plan
            for plan in execution_plans
            if plan["execution_action"] == "REQUIRE_HUMAN_REVIEW"
        ]

        blocked_deals = [
            plan
            for plan in execution_plans
            if plan["execution_action"] == "DO_NOT_EXECUTE"
        ]

        return {
            "total_deals": len(execution_plans),
            "execution_plans": execution_plans,
            "executable_deals": executable_deals,
            "review_required": review_required,
            "blocked_deals": blocked_deals,
            "executable_count": len(executable_deals),
            "review_count": len(review_required),
            "blocked_count": len(blocked_deals),
            "status": "DECISION_EXECUTION_EVALUATION_COMPLETE",
        }
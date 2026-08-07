from __future__ import annotations

from typing import Any, Dict

from .decision_execution_engine import DecisionExecutionEngine


class DecisionExecutionIntegration:
    """
    Integrates policy enforcement with executable acquisition decisions.
    """

    def __init__(
        self,
        execution_engine: DecisionExecutionEngine | None = None,
    ) -> None:
        self.execution_engine = (
            execution_engine
            if execution_engine is not None
            else DecisionExecutionEngine()
        )

    def evaluate(
        self,
        enforcement_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not isinstance(enforcement_results, dict):
            raise TypeError("enforcement_results must be a dictionary")

        result = self.execution_engine.evaluate(
            enforcement_results
        )

        return {
            "enforcement_results": enforcement_results,
            "execution": result,
            "executable_deals": result["executable_deals"],
            "review_required": result["review_required"],
            "blocked_deals": result["blocked_deals"],
            "status": "DECISION_EXECUTION_INTEGRATION_COMPLETE",
        }
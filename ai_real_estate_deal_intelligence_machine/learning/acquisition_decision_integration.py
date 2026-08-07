from __future__ import annotations

from typing import Any, Dict, List

from ai_real_estate_deal_intelligence_machine.learning.acquisition_decision_engine import (
    AcquisitionDecisionEngine,
)

from ai_real_estate_deal_intelligence_machine.learning.acquisition_strategy_engine import (
    AcquisitionStrategyEngine,
)


class AcquisitionDecisionIntegration:
    """
    Integrates acquisition decision intelligence.

    Sprint 4 Part 15:

    Recommendation
          |
          v
    Decision Engine
          |
          v
    Strategy Engine
          |
          v
    Acquisition Workflow
    """

    def __init__(self) -> None:

        self.decision_engine = (
            AcquisitionDecisionEngine()
        )

        self.strategy_engine = (
            AcquisitionStrategyEngine()
        )


    def evaluate(
        self,
        recommendations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluate deal recommendations
        and produce acquisition strategies.
        """

        results = []

        for recommendation in recommendations:

            decision = (
                self.decision_engine.decide(
                    recommendation
                )
            )

            strategy = (
                self.strategy_engine.execute(
                    decision
                )
            )

            results.append(
                {
                    "decision": decision,
                    "strategy": strategy,
                }
            )


        acquire_candidates = [
            result
            for result in results
            if result["decision"]["decision"]
            == "ACQUIRE"
        ]


        return {
            "total_deals": len(
                recommendations
            ),
            "evaluations": results,
            "acquisition_candidates":
                acquire_candidates,
            "status":
                "ACQUISITION_DECISION_INTEGRATION_COMPLETE",
        }
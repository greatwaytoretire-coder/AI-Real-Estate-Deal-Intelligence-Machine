from __future__ import annotations

from typing import Any, Dict, List

from .acquisition_workflow_engine import (
    AcquisitionWorkflowEngine,
)

from .due_diligence_planner import (
    DueDiligencePlanner,
)

from .negotiation_strategy_engine import (
    NegotiationStrategyEngine,
)


class AcquisitionWorkflowIntegration:
    """
    Integrates acquisition execution intelligence.

    Sprint 4 Part 16:

    Decision
       |
       v
    Workflow
       |
       v
    Due Diligence
       |
       v
    Negotiation
       |
       v
    Acquisition Execution Plan
    """

    def __init__(self) -> None:

        self.workflow_engine = (
            AcquisitionWorkflowEngine()
        )

        self.due_diligence_planner = (
            DueDiligencePlanner()
        )

        self.negotiation_engine = (
            NegotiationStrategyEngine()
        )


    def execute(
        self,
        acquisition_candidates: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate complete acquisition
        execution plans.
        """

        results = []


        for candidate in acquisition_candidates:

            decision = candidate.get(
                "decision",
                {}
            )

            strategy = candidate.get(
                "strategy",
                {}
            )


            deal_data = {
                **decision,
                **strategy,
            }


            workflow = (
                self.workflow_engine.generate(
                    deal_data
                )
            )


            due_diligence = (
                self.due_diligence_planner.create_plan(
                    deal_data
                )
            )


            negotiation = (
                self.negotiation_engine.generate_strategy(
                    deal_data
                )
            )


            results.append(
                {
                    "deal_id":
                        deal_data.get(
                            "deal_id"
                        ),

                    "workflow":
                        workflow,

                    "due_diligence":
                        due_diligence,

                    "negotiation":
                        negotiation,

                }
            )


        acquisition_ready = [
            result
            for result in results
            if result["workflow"].get(
                "workflow_status"
            )
            ==
            "ACQUISITION_WORKFLOW_CREATED"
        ]


        return {

            "total_deals":
                len(results),

            "execution_plans":
                results,

            "acquisition_ready":
                acquisition_ready,

            "status":
                "ACQUISITION_WORKFLOW_INTEGRATION_COMPLETE",

        }
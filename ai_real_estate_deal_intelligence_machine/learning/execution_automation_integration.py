from __future__ import annotations

from typing import Any, Dict, List

from ai_real_estate_deal_intelligence_machine.learning.acquisition_task_generator import (
    AcquisitionTaskGenerator,
)

from ai_real_estate_deal_intelligence_machine.learning.seller_communication_planner import (
    SellerCommunicationPlanner,
)

from ai_real_estate_deal_intelligence_machine.learning.follow_up_scheduler import (
    FollowUpScheduler,
)


class ExecutionAutomationIntegration:
    """
    Integrates acquisition execution automation.

    Sprint 4 Part 17:

    Acquisition Decision
            |
            v
    Execution Automation
            |
            v
    Actionable Acquisition Plan
    """

    def __init__(self) -> None:

        self.task_generator = (
            AcquisitionTaskGenerator()
        )

        self.communication_planner = (
            SellerCommunicationPlanner()
        )

        self.follow_up_scheduler = (
            FollowUpScheduler()
        )


    def execute(
        self,
        acquisition_workflows: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate complete execution plans.
        """

        execution_plans = []

        for workflow in acquisition_workflows:

            decision_data = workflow.get(
                "decision",
                {}
            )

            strategy_data = workflow.get(
                "strategy",
                {}
            )


            deal_id = decision_data.get(
                "deal_id",
                "UNKNOWN",
            )


            execution_input = {

                "deal_id":
                    deal_id,

                "decision":
                    decision_data.get(
                        "decision",
                        "MONITOR",
                    ),

                "seller_motivation":
                    strategy_data.get(
                        "seller_motivation",
                        50,
                    ),
            }


            tasks = (
                self.task_generator.generate_tasks(
                    execution_input
                )
            )


            communication = (
                self.communication_planner.generate_plan(
                    execution_input
                )
            )


            schedule = (
                self.follow_up_scheduler.schedule(
                    execution_input
                )
            )


            execution_plans.append(
                {
                    "deal_id":
                        deal_id,

                    "tasks":
                        tasks,

                    "communication":
                        communication,

                    "schedule":
                        schedule,

                }
            )


        acquisition_ready = [

            plan

            for plan in execution_plans

            if plan["tasks"]["decision"]
            ==
            "ACQUIRE"

        ]


        return {

            "total_deals":
                len(
                    execution_plans
                ),

            "execution_plans":
                execution_plans,

            "acquisition_ready":
                acquisition_ready,

            "status":
                "EXECUTION_AUTOMATION_COMPLETE",

        }
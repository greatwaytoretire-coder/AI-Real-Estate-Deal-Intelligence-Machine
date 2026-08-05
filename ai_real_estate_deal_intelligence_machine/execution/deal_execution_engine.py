from __future__ import annotations

from typing import Dict

from ai_real_estate_deal_intelligence_machine.execution.execution_models import (
    DealExecutionPlan,
    ExecutionTask,
)


class DealExecutionEngine:
    """
    Executes the real estate deal workflow.

    Future integrations:
    - CRM automation
    - Email outreach
    - Contract workflows
    - Closing coordination
    """

    DEFAULT_TASKS = [
        "RUN_ACQUISITION_ANALYSIS",
        "RUN_UNDERWRITING",
        "MATCH_BUYERS",
        "GENERATE_DEAL_PACKAGE",
        "EXECUTE_DISPOSITION",
    ]

    def create_execution_plan(
        self,
        property_data: Dict,
    ) -> DealExecutionPlan:

        property_id = property_data.get(
            "property_id",
            "PROP-001",
        )

        tasks = [
            ExecutionTask(task_name=name)
            for name in self.DEFAULT_TASKS
        ]

        return DealExecutionPlan(
            property_id=property_id,
            tasks=tasks,
            status="READY",
        )


    def execute_task(
        self,
        plan: DealExecutionPlan,
        task_name: str,
    ) -> DealExecutionPlan:

        for task in plan.tasks:

            if task.task_name == task_name:

                task.status = "COMPLETED"

                task.result = (
                    f"{task_name} completed successfully."
                )

        completed = all(
            task.status == "COMPLETED"
            for task in plan.tasks
        )

        if completed:
            plan.status = "COMPLETED"
        else:
            plan.status = "IN_PROGRESS"

        return plan
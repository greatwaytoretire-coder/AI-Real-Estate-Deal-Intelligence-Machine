from __future__ import annotations

from typing import Any, Dict, List


class AcquisitionTaskGenerator:
    """
    Generates acquisition execution tasks.

    Sprint 4 Part 17:

    Acquisition Workflow
            |
            v
    Task Generation
            |
            v
    Execution Automation
    """

    def generate_tasks(
        self,
        workflow_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate actionable acquisition tasks.
        """

        deal_id = workflow_data.get(
            "deal_id",
            "UNKNOWN",
        )

        decision = workflow_data.get(
            "decision",
            "MONITOR",
        )


        tasks: List[Dict[str, Any]] = []


        if decision == "ACQUIRE":

            tasks.extend(
                [
                    {
                        "task":
                            "Contact seller",
                        "priority":
                            "HIGH",
                    },
                    {
                        "task":
                            "Schedule property inspection",
                        "priority":
                            "HIGH",
                    },
                    {
                        "task":
                            "Prepare purchase agreement",
                        "priority":
                            "HIGH",
                    },
                    {
                        "task":
                            "Review financing options",
                        "priority":
                            "MEDIUM",
                    },
                ]
            )


        elif decision == "MONITOR":

            tasks.extend(
                [
                    {
                        "task":
                            "Monitor seller motivation",
                        "priority":
                            "MEDIUM",
                    },
                    {
                        "task":
                            "Schedule follow-up review",
                        "priority":
                            "LOW",
                    },
                ]
            )


        else:

            tasks.append(
                {
                    "task":
                        "Archive opportunity",
                    "priority":
                        "LOW",
                }
            )


        return {

            "deal_id":
                deal_id,

            "decision":
                decision,

            "tasks":
                tasks,

            "task_count":
                len(tasks),

            "status":
                "ACQUISITION_TASKS_GENERATED",

        }
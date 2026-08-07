from __future__ import annotations

from typing import Any, Dict, List

from .acquisition_milestone_executor import AcquisitionMilestoneExecutor


class AcquisitionMilestoneExecutionIntegration:
    """
    Coordinates acquisition milestone execution for active acquisitions.
    """

    def __init__(self) -> None:
        self.executor = AcquisitionMilestoneExecutor()

    def evaluate(
        self,
        milestone_plans: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not isinstance(milestone_plans, list):
            raise ValueError("milestone_plans must be a list.")

        execution_results: List[Dict[str, Any]] = []
        active_acquisitions: List[Dict[str, Any]] = []
        completed_acquisitions: List[Dict[str, Any]] = []

        for plan in milestone_plans:
            result = self.executor.execute(plan)
            execution_results.append(result)

            if result.get("execution_state") == "ACQUISITION_COMPLETED":
                completed_acquisitions.append(result)
            else:
                active_acquisitions.append(result)

        return {
            "total_acquisitions": len(execution_results),
            "execution_results": execution_results,
            "active_acquisitions": active_acquisitions,
            "active_count": len(active_acquisitions),
            "completed_acquisitions": completed_acquisitions,
            "completed_count": len(completed_acquisitions),
            "status": "ACQUISITION_MILESTONE_EXECUTION_COMPLETE",
        }
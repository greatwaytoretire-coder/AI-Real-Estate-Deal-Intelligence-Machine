from __future__ import annotations

from typing import Any, Dict, List

from .acquisition_execution_tracker import AcquisitionExecutionTracker
from .acquisition_milestone_engine import AcquisitionMilestoneEngine


class AcquisitionExecutionIntegration:
    """
    Integrates acquisition execution tracking with milestone generation.
    """

    def __init__(self) -> None:
        self.execution_tracker = AcquisitionExecutionTracker()
        self.milestone_engine = AcquisitionMilestoneEngine()

    def evaluate(
        self,
        execution_decisions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluate acquisition execution decisions and generate milestone
        plans for acquisitions that are ready to execute.
        """

        tracking = self.execution_tracker.track(
            execution_decisions
        )

        active_acquisitions = tracking.get(
            "active_acquisitions",
            [],
        )

        milestone_result = self.milestone_engine.generate(
            active_acquisitions
        )

        return {
            "tracking": tracking,
            "milestones": milestone_result,
            "active_acquisitions": active_acquisitions,
            "blocked_acquisitions": tracking.get(
                "blocked_acquisitions",
                [],
            ),
            "review_required": tracking.get(
                "review_required",
                [],
            ),
            "status": "ACQUISITION_EXECUTION_INTEGRATION_COMPLETE",
        }
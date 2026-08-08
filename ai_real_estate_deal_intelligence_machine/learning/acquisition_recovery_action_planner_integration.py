from __future__ import annotations

from typing import Any, Dict

from ai_real_estate_deal_intelligence_machine.learning.acquisition_recovery_action_planner import (
    AcquisitionRecoveryActionPlanner,
)


class AcquisitionRecoveryActionPlanningIntegration:
    """
    Integration boundary for Sprint 4 Part 31.

    Consumes Part 30 resolution results and produces controlled
    recovery action plans. No acquisition action is executed here.
    """

    def __init__(
        self,
        planner: AcquisitionRecoveryActionPlanner | None = None,
    ) -> None:
        self.planner = planner or AcquisitionRecoveryActionPlanner()

    def plan_recovery(
        self,
        resolution_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        result = self.planner.plan_from_resolutions(
            resolution_results
        )

        return result

    def plan_single_recovery(
        self,
        resolution: Dict[str, Any],
    ) -> Dict[str, Any]:
        plan = self.planner.plan_recovery_action(resolution)
        return plan.to_dict()
from __future__ import annotations

from typing import Any, Dict, List


class AcquisitionMilestoneExecutor:
    """
    Executes and advances acquisition milestone plans.

    The engine is intentionally deterministic and side-effect free.
    It evaluates the current milestone state and produces the next
    acquisition execution state.
    """

    MILESTONES = [
        "EXECUTION_INITIATED",
        "SELLER_CONTACT",
        "PROPERTY_DUE_DILIGENCE",
        "NEGOTIATION",
        "PURCHASE_AGREEMENT",
        "ACQUISITION_COMPLETED",
    ]

    def execute(self, milestone_plan: Dict[str, Any]) -> Dict[str, Any]:
        deal_id = milestone_plan.get("deal_id")
        milestones = milestone_plan.get("milestones", [])

        if not deal_id:
            raise ValueError("Milestone plan requires deal_id.")

        if not isinstance(milestones, list):
            raise ValueError("Milestone plan milestones must be a list.")

        if not milestones:
            raise ValueError("Milestone plan must contain at least one milestone.")

        current_index = self._find_current_index(milestones)

        if current_index is None:
            current_index = self._find_first_pending_index(milestones)

        if current_index is None:
            return self._build_completed_result(
                deal_id=deal_id,
                milestones=milestones,
            )

        current = milestones[current_index]

        current["status"] = "COMPLETED"

        next_index = current_index + 1

        if next_index >= len(milestones):
            return self._build_completed_result(
                deal_id=deal_id,
                milestones=milestones,
            )

        next_milestone = milestones[next_index]
        next_milestone["status"] = "CURRENT"

        completed_count = sum(
            1 for milestone in milestones
            if milestone.get("status") == "COMPLETED"
        )

        pending_count = sum(
            1 for milestone in milestones
            if milestone.get("status") == "PENDING"
        )

        return {
            "deal_id": deal_id,
            "execution_state": "ACQUISITION_ACTIVE",
            "current_milestone": next_milestone.get("milestone"),
            "completed_milestone": current.get("milestone"),
            "next_milestone": next_milestone.get("milestone"),
            "completed_count": completed_count,
            "pending_count": pending_count,
            "milestone_count": len(milestones),
            "milestones": milestones,
            "execution_status": "MILESTONE_ADVANCED",
            "status": "ACQUISITION_MILESTONE_EXECUTED",
        }

    def _find_current_index(
        self,
        milestones: List[Dict[str, Any]],
    ) -> int | None:
        for index, milestone in enumerate(milestones):
            if milestone.get("status") == "CURRENT":
                return index

        return None

    def _find_first_pending_index(
        self,
        milestones: List[Dict[str, Any]],
    ) -> int | None:
        for index, milestone in enumerate(milestones):
            if milestone.get("status") == "PENDING":
                return index

        return None

    def _build_completed_result(
        self,
        deal_id: str,
        milestones: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        for milestone in milestones:
            milestone["status"] = "COMPLETED"

        return {
            "deal_id": deal_id,
            "execution_state": "ACQUISITION_COMPLETED",
            "current_milestone": "ACQUISITION_COMPLETED",
            "completed_milestone": "ACQUISITION_COMPLETED",
            "next_milestone": None,
            "completed_count": len(milestones),
            "pending_count": 0,
            "milestone_count": len(milestones),
            "milestones": milestones,
            "execution_status": "ACQUISITION_COMPLETED",
            "status": "ACQUISITION_MILESTONE_EXECUTION_COMPLETE",
        }
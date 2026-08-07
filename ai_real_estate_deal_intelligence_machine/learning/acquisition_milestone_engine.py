from __future__ import annotations

from typing import Any, Dict, List


class AcquisitionMilestoneEngine:
    """
    Generates and evaluates milestones for active acquisition executions.
    """

    DEFAULT_MILESTONES = [
        {
            "milestone": "EXECUTION_INITIATED",
            "description": "Acquisition execution has been initiated.",
            "sequence": 1,
        },
        {
            "milestone": "SELLER_CONTACT",
            "description": "Seller communication and initial acquisition contact completed.",
            "sequence": 2,
        },
        {
            "milestone": "PROPERTY_DUE_DILIGENCE",
            "description": "Property and ownership due diligence completed.",
            "sequence": 3,
        },
        {
            "milestone": "NEGOTIATION",
            "description": "Acquisition negotiation completed.",
            "sequence": 4,
        },
        {
            "milestone": "PURCHASE_AGREEMENT",
            "description": "Purchase agreement prepared and ready for execution.",
            "sequence": 5,
        },
        {
            "milestone": "ACQUISITION_COMPLETED",
            "description": "Acquisition has been completed.",
            "sequence": 6,
        },
    ]

    def generate(
        self,
        active_acquisitions: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate acquisition milestones for active acquisitions.
        """
        execution_plans: List[Dict[str, Any]] = []

        for acquisition in active_acquisitions:
            execution_plans.append(
                self._generate_plan(acquisition)
            )

        return {
            "total_acquisitions": len(active_acquisitions),
            "milestone_plans": execution_plans,
            "status": "ACQUISITION_MILESTONES_GENERATED",
        }

    def _generate_plan(
        self,
        acquisition: Dict[str, Any],
    ) -> Dict[str, Any]:
        deal_id = acquisition.get("deal_id", "UNKNOWN")

        milestones = [
            {
                **milestone,
                "status": (
                    "CURRENT"
                    if milestone["sequence"] == 1
                    else "PENDING"
                ),
            }
            for milestone in self.DEFAULT_MILESTONES
        ]

        return {
            "deal_id": deal_id,
            "execution_state": acquisition.get(
                "execution_state",
                "ACQUISITION_ACTIVE",
            ),
            "current_milestone": "EXECUTION_INITIATED",
            "milestones": milestones,
            "milestone_count": len(milestones),
            "completed_count": 0,
            "pending_count": len(milestones) - 1,
            "next_milestone": "SELLER_CONTACT",
            "status": "ACQUISITION_MILESTONE_PLAN_CREATED",
        }

    def update_progress(
        self,
        milestone_plan: Dict[str, Any],
        completed_milestone: str,
    ) -> Dict[str, Any]:
        """
        Advance an acquisition milestone plan by marking a milestone
        complete and selecting the next pending milestone.
        """
        milestones = milestone_plan.get("milestones", [])

        completed_found = False

        for milestone in milestones:
            if milestone.get("milestone") == completed_milestone:
                milestone["status"] = "COMPLETED"
                completed_found = True

        if not completed_found:
            return {
                **milestone_plan,
                "status": "MILESTONE_NOT_FOUND",
            }

        pending = [
            milestone
            for milestone in milestones
            if milestone.get("status") != "COMPLETED"
        ]

        if pending:
            next_milestone = min(
                pending,
                key=lambda item: item.get("sequence", 999),
            )

            next_milestone["status"] = "CURRENT"

            current_milestone = next_milestone["milestone"]
            next_milestone_name = current_milestone
        else:
            current_milestone = "ACQUISITION_COMPLETED"
            next_milestone_name = None

        completed_count = sum(
            1
            for milestone in milestones
            if milestone.get("status") == "COMPLETED"
        )

        pending_count = len(milestones) - completed_count

        return {
            **milestone_plan,
            "current_milestone": current_milestone,
            "next_milestone": next_milestone_name,
            "completed_count": completed_count,
            "pending_count": pending_count,
            "status": "ACQUISITION_MILESTONE_PROGRESS_UPDATED",
        }
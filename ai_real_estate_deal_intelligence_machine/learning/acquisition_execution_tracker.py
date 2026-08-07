from __future__ import annotations

from typing import Any, Dict, List


class AcquisitionExecutionTracker:
    """
    Tracks the execution state of acquisition decisions.

    This component receives decision-execution plans and converts them
    into acquisition execution states that can be consumed by the
    milestone and integration layers.
    """

    STATUS_READY = "READY_FOR_EXECUTION"
    STATUS_ACTIVE = "ACQUISITION_EXECUTION_ACTIVE"
    STATUS_BLOCKED = "EXECUTION_BLOCKED"
    STATUS_REVIEW = "HUMAN_REVIEW_REQUIRED"

    def track(self, execution_decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Track acquisition execution decisions.

        Args:
            execution_decisions:
                Decision execution records produced by Sprint 4 Part 22.

        Returns:
            A structured execution tracking result.
        """
        tracked_executions: List[Dict[str, Any]] = []
        active_acquisitions: List[Dict[str, Any]] = []
        blocked_acquisitions: List[Dict[str, Any]] = []
        review_required: List[Dict[str, Any]] = []

        for decision in execution_decisions:
            tracked = self._track_decision(decision)
            tracked_executions.append(tracked)

            status = tracked["execution_status"]

            if status == self.STATUS_ACTIVE:
                active_acquisitions.append(tracked)
            elif status == self.STATUS_BLOCKED:
                blocked_acquisitions.append(tracked)
            elif status == self.STATUS_REVIEW:
                review_required.append(tracked)

        return {
            "total_decisions": len(execution_decisions),
            "tracked_executions": tracked_executions,
            "active_acquisitions": active_acquisitions,
            "blocked_acquisitions": blocked_acquisitions,
            "review_required": review_required,
            "active_count": len(active_acquisitions),
            "blocked_count": len(blocked_acquisitions),
            "review_count": len(review_required),
            "status": "ACQUISITION_EXECUTION_TRACKING_COMPLETE",
        }

    def _track_decision(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        deal_id = decision.get("deal_id", "UNKNOWN")
        enforcement_decision = decision.get("enforcement_decision")
        execution_action = decision.get("execution_action")
        recommendation = decision.get("recommendation")
        risk_level = decision.get("risk_level")

        if enforcement_decision == "APPROVE" and execution_action == "EXECUTE_ACQUISITION":
            execution_status = self.STATUS_ACTIVE
            execution_state = "ACQUISITION_ACTIVE"
            next_step = "Begin acquisition milestone tracking."
        elif enforcement_decision == "REVIEW":
            execution_status = self.STATUS_REVIEW
            execution_state = "HUMAN_REVIEW"
            next_step = "Obtain human approval before beginning acquisition execution."
        else:
            execution_status = self.STATUS_BLOCKED
            execution_state = "ACQUISITION_BLOCKED"
            next_step = "Do not execute acquisition; retain opportunity for future learning."

        return {
            "deal_id": deal_id,
            "enforcement_decision": enforcement_decision,
            "execution_action": execution_action,
            "execution_status": execution_status,
            "execution_state": execution_state,
            "recommendation": recommendation,
            "risk_level": risk_level,
            "next_step": next_step,
            "status": "ACQUISITION_EXECUTION_TRACKED",
        }
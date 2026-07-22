from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List
from uuid import uuid4

from .audit_logger import AuditLogger


class ApprovalStatus(str, Enum):
    """Defines the lifecycle of an action requiring human approval."""

    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class AuditEntry:
    """An entry in the audit history of an approval action."""

    timestamp: str
    status: ApprovalStatus
    notes: str
    operator_id: str = "system"


@dataclass
class ActionForApproval:
    """A comprehensive package for a human to review and approve an AI-recommended action."""

    action_id: str = field(default_factory=lambda: f"action_{uuid4()}")
    status: ApprovalStatus = ApprovalStatus.DRAFT
    action_type: str = "GENERIC_ACTION"
    recommendation: str = ""
    reasoning: str = ""
    supporting_data: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.0
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    action_payload: Dict[str, Any] = field(default_factory=dict)
    audit_history: List[AuditEntry] = field(default_factory=list)

    def __post_init__(self):
        if not self.audit_history:
            self._add_audit_entry(self.status, "Action created.")

    def _add_audit_entry(self, status: ApprovalStatus, notes: str, operator_id: str = "system"):
        self.audit_history.append(
            AuditEntry(timestamp=datetime.utcnow().isoformat(), status=status, notes=notes, operator_id=operator_id)
        )


class HumanInTheLoopEngine:
    """Manages the queue and lifecycle of actions requiring human approval."""

    def __init__(self, audit_logger: AuditLogger):
        self.approval_queue: List[ActionForApproval] = []
        self.audit_logger = audit_logger

    def submit_for_approval(self, action: ActionForApproval):
        """Submits a new action to the approval queue."""
        action.status = ApprovalStatus.PENDING_REVIEW
        action._add_audit_entry(ApprovalStatus.PENDING_REVIEW, "Submitted for human review.")
        self.approval_queue.append(action)
        self.audit_logger.log("APPROVAL_WORKFLOW", f"Action {action.action_id} submitted for review.")

    def _find_action(self, action_id: str) -> ActionForApproval | None:
        return next((a for a in self.approval_queue if a.action_id == action_id), None)

    def approve(self, action_id: str, operator_id: str, notes: str = "Approved by operator."):
        action = self._find_action(action_id)
        if action and action.status == ApprovalStatus.PENDING_REVIEW:
            action.status = ApprovalStatus.APPROVED
            action._add_audit_entry(ApprovalStatus.APPROVED, notes, operator_id)
            self.audit_logger.log("APPROVAL_WORKFLOW", f"Action {action_id} approved by {operator_id}.")
            # In a real system, this would trigger an execution workflow
            return True
        return False

    def reject(self, action_id: str, operator_id: str, notes: str = "Rejected by operator."):
        action = self._find_action(action_id)
        if action and action.status == ApprovalStatus.PENDING_REVIEW:
            action.status = ApprovalStatus.REJECTED
            action._add_audit_entry(ApprovalStatus.REJECTED, notes, operator_id)
            self.audit_logger.log("APPROVAL_WORKFLOW", f"Action {action_id} rejected by {operator_id}.")
            return True
        return False

    def edit(self, action_id: str, operator_id: str, new_payload: Dict[str, Any]):
        action = self._find_action(action_id)
        if action and action.status == ApprovalStatus.PENDING_REVIEW:
            action.action_payload = new_payload
            action._add_audit_entry(ApprovalStatus.DRAFT, "Action edited by operator.", operator_id)
            action.status = ApprovalStatus.PENDING_REVIEW  # Must be re-reviewed
            action._add_audit_entry(ApprovalStatus.PENDING_REVIEW, "Resubmitted after edit.")
            self.audit_logger.log("APPROVAL_WORKFLOW", f"Action {action_id} edited by {operator_id}.")
            return True
        return False

    def cancel(self, action_id: str, operator_id: str, notes: str = "Cancelled by operator."):
        action = self._find_action(action_id)
        if action and action.status in [ApprovalStatus.DRAFT, ApprovalStatus.PENDING_REVIEW]:
            action.status = ApprovalStatus.CANCELLED
            action._add_audit_entry(ApprovalStatus.CANCELLED, notes, operator_id)
            self.audit_logger.log("APPROVAL_WORKFLOW", f"Action {action_id} cancelled by {operator_id}.")
            return True
        return False


class PendingActionDashboard:
    """Provides a view of actions awaiting human review."""

    def __init__(self, engine: HumanInTheLoopEngine):
        self.engine = engine

    def generate_report(self) -> List[Dict[str, Any]]:
        """Returns a list of actions pending review."""
        pending_actions = [a for a in self.engine.approval_queue if a.status == ApprovalStatus.PENDING_REVIEW]
        return [
            {
                "action_id": action.action_id,
                "action_type": action.action_type,
                "recommendation": action.recommendation,
                "confidence": action.confidence_score,
            }
            for action in pending_actions
        ]
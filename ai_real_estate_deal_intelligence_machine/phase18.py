from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class GuardrailDecision:
    agent: str
    trigger: str
    input_data: Dict[str, Any]
    decision: str
    action: str
    result: str
    timestamp: str = ""

    def as_dict(self) -> Dict[str, Any]:
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        return {
            "agent": self.agent,
            "trigger": self.trigger,
            "input": self.input_data,
            "decision": self.decision,
            "action": self.action,
            "result": self.result,
            "timestamp": self.timestamp,
        }


@dataclass
class ComplianceAuditTrail:
    agent: str
    trigger: str
    input_data: Dict[str, Any]
    decision: str
    action: str
    result: str
    timestamp: str = ""

    def as_dict(self) -> Dict[str, Any]:
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
        return {
            "agent": self.agent,
            "trigger": self.trigger,
            "input": self.input_data,
            "decision": self.decision,
            "action": self.action,
            "result": self.result,
            "timestamp": self.timestamp,
        }


class ComplianceGuardrailAgent:
    """Phase 18 compliance guardrail foundation."""

    def evaluate_action(
        self,
        agent_name: str,
        trigger: str,
        input_data: Dict[str, Any],
        decision: str,
        action: str,
        result: str,
    ) -> Dict[str, Any]:
        allowed = decision != "block"
        trail = ComplianceAuditTrail(
            agent=agent_name,
            trigger=trigger,
            input_data=input_data,
            decision=decision,
            action=action,
            result=result,
        )
        return {
            "allowed": allowed,
            "decision": decision,
            "action": action,
            "result": result,
            "audit": trail.as_dict(),
        }

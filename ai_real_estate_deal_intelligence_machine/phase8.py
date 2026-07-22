from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict

from .audit_logger import AuditLogger
from .phase36 import AgentContract, AgentInput, AgentOutput, AIAgent


@dataclass
class RiskAssessment:
    risk_score: int
    critical_risk: bool
    warning: str
    information_gap: str


@dataclass
class DealRiskAgentInput(AgentInput):
    """Inputs required for the DealRiskAgent."""
    deal_id: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "risk_score": self.risk_score,
            "critical_risk": self.critical_risk,
            "warning": self.warning,
            "information_gap": self.information_gap,
        }


@dataclass
class DealRiskAgentOutput(AgentOutput):
    """Outputs from the DealRiskAgent."""
    assessment: RiskAssessment | None = None


class DealRiskAgent(AIAgent):
    """Phase 8 risk-evaluation foundation for deal suppression and verification."""

    def get_contract(self) -> AgentContract:
        return AgentContract(
            agent_name="DealRiskAgent",
            purpose="To evaluate the risk factors of a deal and produce a risk score and mitigation plan.",
            version="2.0.0",
            input_schema={"deal_id": "string"},
            output_schema={"assessment": "RiskAssessment"},
        )

    def execute(self, agent_input: DealRiskAgentInput) -> DealRiskAgentOutput:
        self.audit_logger.log("AGENT_EXECUTE_START", f"DealRiskAgent starting for correlation_id: {agent_input.correlation_id}")

        try:
            # In a real system, we would use agent_input.deal_id to fetch deal data.
            # Here, we continue to use the mock logic for demonstration.
            assessment = self._evaluate_risk()
            output = DealRiskAgentOutput(confidence=0.9, assessment=assessment)
            self.audit_logger.log("AGENT_EXECUTE_SUCCESS", f"DealRiskAgent finished for correlation_id: {agent_input.correlation_id}")
            return output
        except Exception as e:
            return DealRiskAgentOutput(confidence=0.0, error=str(e))

    def _evaluate_risk(self) -> RiskAssessment:
        """Original mock logic, now a private method."""
        return RiskAssessment(
            risk_score=72,
            critical_risk=True,
            warning="Insufficient spread and weak buyer demand",
            information_gap="Buyer demand snapshot missing",
        )

        return {
            "risk_score": assessment.risk_score,
            "critical_risk": assessment.critical_risk,
            "warning": assessment.warning,
            "information_gap": assessment.information_gap,
            "alert_created": True,
            "priority_reduced": True,
            "recommended_verification_task": "Verify buyer demand and spread before promotion",
            "auto_promotion_blocked": True,
        }

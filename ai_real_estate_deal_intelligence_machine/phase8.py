from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from .audit_logger import AuditLogger
from .agents.base import AgentContract, AgentInput, AgentOutput, AIAgent


@dataclass
class RiskAssessment:
    risk_score: int
    critical_risk: bool
    warning: str
    information_gap: str

    def as_dict(self) -> Dict[str, Any]:
        """Serializes the dataclass to a dictionary."""
        return asdict(self)


@dataclass
class DealRiskAgentInput(AgentInput):
    """Inputs required for the DealRiskAgent."""
    deal_id: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "market_id": self.market_id,
            "deal_id": self.deal_id,
        }


@dataclass
class DealRiskAgentOutput(AgentOutput):
    """Outputs from the DealRiskAgent."""
    assessment: RiskAssessment | None = None


class DealRiskAgent(AIAgent):
    """Phase 8 risk-evaluation foundation for deal suppression and verification."""

    def __init__(
        self,
        audit_logger: Optional[AuditLogger] = None,
    ) -> None:
        super().__init__(audit_logger)

    def get_contract(self) -> AgentContract:
        return AgentContract(
            agent_name="DealRiskAgent",
            purpose=(
                "To evaluate the risk factors of a deal and "
                "produce a risk score and mitigation plan."
            ),
            version="2.0.0",
            input_schema={
                "deal_id": "string",
            },
            output_schema={
                "assessment": "RiskAssessment",
            },
        )

    def execute(
        self,
        agent_input: DealRiskAgentInput,
    ) -> DealRiskAgentOutput:
        self.audit_logger.log(
            "AGENT_EXECUTE_START",
            (
                "DealRiskAgent starting for "
                f"correlation_id: {agent_input.correlation_id}"
            ),
        )

        try:
            assessment = self._evaluate_risk()

            output = DealRiskAgentOutput(
                confidence=0.9,
                assessment=assessment,
            )

            self.audit_logger.log(
                "AGENT_EXECUTE_SUCCESS",
                (
                    "DealRiskAgent finished for "
                    f"correlation_id: {agent_input.correlation_id}"
                ),
            )

            return output

        except Exception as error:
            return DealRiskAgentOutput(
                confidence=0.0,
                error=str(error),
            )

    def _evaluate_risk(self) -> RiskAssessment:
        """Evaluates the risk of a deal using mock risk logic."""

        return RiskAssessment(
            risk_score=72,
            critical_risk=True,
            warning=(
                "Insufficient spread and weak buyer demand"
            ),
            information_gap=(
                "Buyer demand snapshot missing"
            ),
        )
    def evaluate_risk(self) -> Dict[str, Any]:
        """Return the legacy dictionary risk-evaluation interface."""

        assessment = self._evaluate_risk()
        result = assessment.as_dict()
        result["auto_promotion_blocked"] = assessment.critical_risk
        return result
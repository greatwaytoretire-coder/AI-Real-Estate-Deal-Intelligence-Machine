from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .audit_logger import AuditLogger
from .phase36 import AgentContract, AgentInput, AgentOutput, AIAgent
from .phase4 import PropertyProfile
from .phase29 import ScalingManager # Assuming a way to access this

@dataclass
class DealScorecard:
    opportunity_score: float = 84.0
    deal_potential_score: float = 78.0
    market_score: float = 81.0
    buyer_demand_score: float = 77.0
    risk_score: float = 22.0
    data_confidence_score: float = 88.0
    urgency_score: float = 70.0

    def as_dict(self) -> Dict[str, float]:
        return {
            "opportunity_score": self.opportunity_score,
            "deal_potential_score": self.deal_potential_score,
            "market_score": self.market_score,
            "buyer_demand_score": self.buyer_demand_score,
            "risk_score": self.risk_score,
            "data_confidence_score": self.data_confidence_score,
            "urgency_score": self.urgency_score,
        }


class PriorityDealQueue:
    def __init__(self) -> None:
        self.items: List[Dict[str, Any]] = []

    def push(self, item: Dict[str, Any]) -> None:
        self.items.append(item)

    def ranked(self) -> List[Dict[str, Any]]:
        return sorted(self.items, key=lambda entry: entry["priority"], reverse=True)


@dataclass
class ScoringInput(AgentInput):
    """Inputs for the scoring engine."""
    property_profile: PropertyProfile


@dataclass
class ScoringOutput(AgentOutput):
    """Outputs from the scoring engine."""
    scorecard: Optional[DealScorecard] = None


class OpportunityScoringEngine(AIAgent):
    """Phase 5 explainable opportunity scoring foundation."""

    def __init__(self, audit_logger: AuditLogger) -> None:
        super().__init__(audit_logger)
        self.priority_queue = PriorityDealQueue()

    def get_contract(self) -> AgentContract:
        return AgentContract(
            agent_name="OpportunityScoringEngine",
            purpose="To score a deal's potential and prioritize it for review.",
            version="2.0.0",
            input_schema={"property_profile": "PropertyProfile"},
            output_schema={"scorecard": "DealScorecard"},
        )

    def execute(self, agent_input: ScoringInput) -> ScoringOutput:
        """Executes the scoring logic."""
        self.audit_logger.log("AGENT_EXECUTE_START", f"OpportunityScoringEngine starting for correlation_id: {agent_input.correlation_id}")

        # Simulate using market-specific scoring
        market_id = agent_input.market_id
        scoring_model_version = "default_v1" # Default
        # In a real system, we'd fetch the market config:
        # scaling_manager = ScalingManager() # This would be injected
        # market_config = scaling_manager.get_market_config(market_id)
        # if market_config:
        #     scoring_model_version = market_config.scoring_model_version

        scorecard = DealScorecard()
        if scoring_model_version == "austin_v2": # Simulate different logic
            scorecard.deal_potential_score = 95.0 # Austin gets a higher score

        self.audit_logger.log("AGENT_EXECUTE_SUCCESS", f"Scoring complete for market '{market_id}' using model '{scoring_model_version}'.")
        return ScoringOutput(confidence=0.9, scorecard=scorecard)

    def _promote_high_scoring(self, queue: PriorityDealQueue) -> List[Dict[str, Any]]:
        """Original mock logic, now a private method."""
        promoted: List[Dict[str, Any]] = []
        scorecard = self.scorecard.as_dict()
        high_priority = 0
        for name, value in scorecard.items():
            if name in {"opportunity_score", "deal_potential_score", "buyer_demand_score", "market_score"} and value >= 70:
                high_priority += 1

        entry = {
            "deal_id": "deal-001",
            "priority": max(0, high_priority * 15),
            "scorecard": scorecard,
        }
        queue.push(entry)
        promoted.append(entry)
        return promoted

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .agents.base import (
    AIAgent,
    AgentContract,
    AgentInput,
    AgentOutput,
)
from .audit_logger import AuditLogger
from .phase4 import PropertyProfile


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
        return sorted(
            self.items,
            key=lambda entry: entry["priority"],
            reverse=True,
        )


@dataclass
class ScoringInput(AgentInput):
    """Inputs for the scoring engine."""

    property_profile: Optional[PropertyProfile] = None
    scoring_model_version: str = "default_v1"


@dataclass
class ScoringOutput(AgentOutput):
    """Outputs from the scoring engine."""

    scorecard: Optional[DealScorecard] = None


class OpportunityScoringEngine(AIAgent):
    """Phase 5 explainable opportunity scoring foundation."""

    def __init__(
        self,
        audit_logger: Optional[AuditLogger] = None,
    ) -> None:
        super().__init__(audit_logger)
        self.priority_queue = PriorityDealQueue()

    def get_contract(self) -> AgentContract:
        return AgentContract(
            agent_name="OpportunityScoringEngine",
            purpose=(
                "To score a deal's potential and "
                "prioritize it for review."
            ),
            version="2.0.0",
            input_schema={
                "property_profile": "PropertyProfile",
            },
            output_schema={
                "scorecard": "DealScorecard",
            },
        )

    def execute(
        self,
        agent_input: ScoringInput,
    ) -> ScoringOutput:
        """Executes the scoring logic."""

        self.audit_logger.log(
            "AGENT_EXECUTE_START",
            (
                "OpportunityScoringEngine starting for "
                f"correlation_id: "
                f"{agent_input.correlation_id}"
            ),
        )

        market_id = agent_input.market_id
        scoring_model_version = (
            agent_input.scoring_model_version
        )

        scorecard = DealScorecard()

        if scoring_model_version == "austin_v2":
            scorecard.deal_potential_score = 95.0

        self.audit_logger.log(
            "AGENT_EXECUTE_SUCCESS",
            (
                "Scoring complete for market "
                f"'{market_id}' using model "
                f"'{scoring_model_version}'."
            ),
        )

        return ScoringOutput(
            confidence=0.9,
            scorecard=scorecard,
        )

    def promote_high_scoring(
        self,
        queue: PriorityDealQueue,
    ) -> List[Dict[str, Any]]:
        """Promotes high-scoring opportunities into the queue."""

        promoted: List[Dict[str, Any]] = []

        scorecard = DealScorecard().as_dict()

        high_priority = 0

        qualifying_scores = {
            "opportunity_score",
            "deal_potential_score",
            "buyer_demand_score",
            "market_score",
        }

        for name, value in scorecard.items():
            if name in qualifying_scores and value >= 70:
                high_priority += 1

        entry = {
            "deal_id": "deal-001",
            "priority": max(0, high_priority * 15),
            "scorecard": scorecard,
        }

        queue.push(entry)
        promoted.append(entry)

        return promoted
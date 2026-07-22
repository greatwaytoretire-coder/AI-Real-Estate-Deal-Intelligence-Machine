from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class DealLifecycleStage(str, Enum):
    DISCOVERED = "DISCOVERED"
    ANALYZING = "ANALYZING"
    QUALIFIED = "QUALIFIED"
    SELLER_ENGAGED = "SELLER ENGAGED"
    UNDERWRITING = "UNDERWRITING"
    OFFER = "OFFER"
    NEGOTIATION = "NEGOTIATION"
    UNDER_CONTRACT = "UNDER CONTRACT"
    DUE_DILIGENCE = "DUE DILIGENCE"
    DEAL_ROOM = "DEAL ROOM"
    BUYER_INTEREST = "BUYER INTEREST"
    OFFERS = "OFFERS"
    DISPOSITION = "DISPOSITION"
    CLOSED = "CLOSED"
    OUTCOME_RECORDED = "OUTCOME RECORDED"


@dataclass
class DealLifecycleWorkflow:
    current_stage: DealLifecycleStage = DealLifecycleStage.DISCOVERED
    tasks: List[str] = field(default_factory=lambda: ["Analyze deal", "Create next best action"])
    alerts: List[str] = field(default_factory=lambda: ["Watch for stalled progression"])

    def as_dict(self) -> Dict[str, Any]:
        return {
            "current_stage": self.current_stage.value,
            "tasks": self.tasks,
            "alerts": self.alerts,
        }


class NextBestActionEngine:
    """Phase 14 next best action foundation for lifecycle progression."""

    def recommend_next_actions(self, workflow: DealLifecycleWorkflow) -> List[Dict[str, str]]:
        return [
            {
                "title": "Next Best Action",
                "action": f"Advance from {workflow.current_stage.value} to {DealLifecycleStage.ANALYZING.value}",
                "reason": "Initialize analysis and queue the next task",
            }
        ]

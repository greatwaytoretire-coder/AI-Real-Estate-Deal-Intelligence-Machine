from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class SellerStage(str, Enum):
    DISCOVERED = "Discovered"
    RESEARCHING = "Researching"
    CONTACTING = "Contacting"
    ENGAGED = "Engaged"
    QUALIFIED = "Qualified"
    NEGOTIATING = "Negotiating"
    OFFER = "Offer"
    CONTRACT = "Contract"
    CLOSED = "Closed"
    LOST = "Lost"


@dataclass
class SellerOpportunity:
    seller_id: str
    stage: SellerStage
    priority: str
    signal_summary: str
    missing_information: List[str]
    opt_out: bool
    communication_preference: str


@dataclass
class SellerQualificationPlan:
    seller_id: str
    steps: List[str]
    legal_requirements: List[str]
    rate_limit_policy: str
    outreach_channel: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "seller_id": self.seller_id,
            "steps": self.steps,
            "legal_requirements": self.legal_requirements,
            "rate_limit_policy": self.rate_limit_policy,
            "outreach_channel": self.outreach_channel,
        }


class SellerAcquisitionAgent:
    """Phase 11 seller acquisition foundation."""

    def identify_high_priority_opportunity(self) -> SellerOpportunity:
        return SellerOpportunity(
            seller_id="seller-001",
            stage=SellerStage.DISCOVERED,
            priority="HIGH",
            signal_summary="Owner has high equity, distressed, and recent maintenance concerns",
            missing_information=["seller motivation", "property condition evidence"],
            opt_out=False,
            communication_preference="email",
        )

    def build_qualification_plan(self, opportunity: SellerOpportunity) -> SellerQualificationPlan:
        return SellerQualificationPlan(
            seller_id=opportunity.seller_id,
            steps=[
                "Verify seller ownership and motivation",
                "Gather property condition signals",
                "Confirm communication preference and consent",
                "Prepare personalized outreach",
            ],
            legal_requirements=["Respect opt-outs", "Honor communication preference", "Respect rate limits"],
            rate_limit_policy="Do not exceed one outbound message per seller per 24 hours",
            outreach_channel=opportunity.communication_preference,
        )

    def generate_outreach(self, opportunity: SellerOpportunity) -> List[str]:
        return [
            f"Personalized outreach for {opportunity.seller_id} via {opportunity.communication_preference}",
            "Monitor response and classify intent",
            "Schedule follow-up if no response",
        ]

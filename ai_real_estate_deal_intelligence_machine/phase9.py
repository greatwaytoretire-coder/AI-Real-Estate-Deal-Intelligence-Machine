from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class BuyerProfile:
    """Buyer identity profile with evidence-gated verification semantics."""

    buyer_id: str
    geography: str
    purchase_range: Tuple[float, float]
    property_type: str
    strategy: str
    proof_of_funds: Optional[str] = None
    verification_status: str = "UNVERIFIED"
    source_authority: str = "mock-authorized-source"

    @property
    def verified(self) -> bool:
        return self.verification_status == "VERIFIED" and bool(self.proof_of_funds)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "buyer_id": self.buyer_id,
            "geography": self.geography,
            "purchase_range": self.purchase_range,
            "property_type": self.property_type,
            "strategy": self.strategy,
            "proof_of_funds": self.proof_of_funds,
            "verification_status": self.verification_status,
            "source_authority": self.source_authority,
            "verified": self.verified,
        }


@dataclass
class BuyerActivityProfile:
    buyer_id: str
    transaction_activity: int
    recent_activity: str
    activity_window: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "buyer_id": self.buyer_id,
            "transaction_activity": self.transaction_activity,
            "recent_activity": self.recent_activity,
            "activity_window": self.activity_window,
        }


@dataclass
class BuyerMatchScore:
    buyer_id: str
    overall_score: float
    geography_fit: float
    price_fit: float
    strategy_fit: float
    notes: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "buyer_id": self.buyer_id,
            "overall_score": round(self.overall_score, 2),
            "geography_fit": round(self.geography_fit, 2),
            "price_fit": round(self.price_fit, 2),
            "strategy_fit": round(self.strategy_fit, 2),
            "notes": self.notes,
        }


@dataclass
class BuyerReliabilityScore:
    buyer_id: str
    reliability_score: float
    verified: bool
    evidence_count: int
    warning: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "buyer_id": self.buyer_id,
            "reliability_score": round(self.reliability_score, 2),
            "verified": self.verified,
            "evidence_count": self.evidence_count,
            "warning": self.warning,
        }


@dataclass
class BuyerIntelligenceEvent:
    event_type: str
    payload: Dict[str, Any]


class BuyerIntelligenceEngine:
    """Phase 9 buyer discovery and intelligence foundation."""

    def discover_buyer(self, buyer_id: str = "buyer-0001") -> BuyerProfile:
        return BuyerProfile(
            buyer_id=buyer_id,
            geography="Austin, TX",
            purchase_range=(150000, 260000),
            property_type="single-family",
            strategy="fix-and-flip",
            proof_of_funds="bank statement snapshot",
            verification_status="VERIFIED",
            source_authority="mock-authorized-source",
        )

    def build_activity_profile(self, buyer_id: str = "buyer-0001") -> BuyerActivityProfile:
        return BuyerActivityProfile(
            buyer_id=buyer_id,
            transaction_activity=6,
            recent_activity="closed 2 deals in the last 90 days",
            activity_window="90 days",
        )

    def score_match(self, buyer_id: str = "buyer-0001") -> BuyerMatchScore:
        return BuyerMatchScore(
            buyer_id=buyer_id,
            overall_score=83.5,
            geography_fit=88.0,
            price_fit=80.0,
            strategy_fit=85.0,
            notes=["Strong geography alignment", "Purchase range is consistent"],
        )

    def score_reliability(self, buyer_id: str = "buyer-0001") -> BuyerReliabilityScore:
        buyer = self.discover_buyer(buyer_id)
        verified = buyer.verified
        return BuyerReliabilityScore(
            buyer_id=buyer_id,
            reliability_score=92.0 if verified else 40.0,
            verified=verified,
            evidence_count=1 if verified else 0,
            warning="" if verified else "Buyer cannot be marked verified without supporting evidence",
        )

    def generate_event(self, buyer_id: str = "buyer-0001") -> BuyerIntelligenceEvent:
        buyer = self.discover_buyer(buyer_id)
        activity = self.build_activity_profile(buyer_id)
        match_score = self.score_match(buyer_id)
        reliability = self.score_reliability(buyer_id)

        payload = {
            "buyer": buyer.as_dict(),
            "activity": activity.as_dict(),
            "match_score": match_score.as_dict(),
            "reliability": reliability.as_dict(),
        }

        return BuyerIntelligenceEvent(event_type="BUYER_INTELLIGENCE_UPDATED", payload=payload)

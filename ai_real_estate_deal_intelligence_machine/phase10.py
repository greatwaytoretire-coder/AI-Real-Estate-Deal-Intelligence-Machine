from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BuyerMatchOpportunity:
    buyer_id: str
    score: float
    category: str
    reason: str
    location: str = ""
    price: str = ""
    property_type: str = ""
    strategy: str = ""
    repair_profile: str = ""
    arv: str = ""
    historical_behavior: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "buyer_id": self.buyer_id,
            "score": round(self.score, 2),
            "category": self.category,
            "reason": self.reason,
            "location": self.location,
            "price": self.price,
            "property_type": self.property_type,
            "strategy": self.strategy,
            "repair_profile": self.repair_profile,
            "arv": self.arv,
            "historical_behavior": self.historical_behavior,
        }


@dataclass
class BuyerRankedMatch:
    top_10_buyer_matches: List[BuyerMatchOpportunity]
    top_verified_buyers: List[BuyerMatchOpportunity]
    top_high_reliability_buyers: List[BuyerMatchOpportunity]
    top_recently_active_buyers: List[BuyerMatchOpportunity]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "TOP 10 BUYER MATCHES": [item.as_dict() for item in self.top_10_buyer_matches],
            "TOP VERIFIED BUYERS": [item.as_dict() for item in self.top_verified_buyers],
            "TOP HIGH-RELIABILITY BUYERS": [item.as_dict() for item in self.top_high_reliability_buyers],
            "TOP RECENTLY ACTIVE BUYERS": [item.as_dict() for item in self.top_recently_active_buyers],
        }


class BuyerMatchingEngine:
    """Phase 10 buyer matching foundation for ranking and outreach opportunities."""

    def __init__(self) -> None:
        self._buyer_database: List[Dict[str, Any]] = [
            {
                "buyer_id": "buyer-0001",
                "location": "Austin, TX",
                "price": "150000-260000",
                "property_type": "single-family",
                "strategy": "fix-and-flip",
                "repair_profile": "light rehab",
                "arv": "210000-240000",
                "historical_behavior": "closed 2 deals in 90 days",
                "verified": True,
                "reliability_score": 93.0,
                "recent_activity": "closed 2 deals in the last 90 days",
                "transaction_activity": 6,
                "proof_of_funds": "bank statement snapshot",
            },
            {
                "buyer_id": "buyer-0002",
                "location": "Dallas, TX",
                "price": "200000-320000",
                "property_type": "multi-family",
                "strategy": "buy-and-hold",
                "repair_profile": "moderate rehab",
                "arv": "250000-300000",
                "historical_behavior": "active in the last 30 days",
                "verified": False,
                "reliability_score": 72.0,
                "recent_activity": "made 4 offers in the last 30 days",
                "transaction_activity": 4,
                "proof_of_funds": None,
            },
        ]

    def search_buyer_database(
        self,
        location: Optional[str] = None,
        price_range: Optional[str] = None,
        property_type: Optional[str] = None,
        strategy: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        candidates = self._buyer_database
        if location:
            candidates = [buyer for buyer in candidates if location.lower() in buyer["location"].lower()]
        if price_range:
            candidates = [buyer for buyer in candidates if price_range == buyer["price"]]
        if property_type:
            candidates = [buyer for buyer in candidates if property_type == buyer["property_type"]]
        if strategy:
            candidates = [buyer for buyer in candidates if strategy == buyer["strategy"]]
        return candidates

    def analyze_buyer_criteria(self, buyer: Dict[str, Any]) -> Dict[str, Any]:
        geography_score = 0.30
        price_score = 0.20 if buyer["price"] else 0.0
        property_type_score = 0.20
        strategy_score = 0.15
        repair_profile_score = 0.10
        arv_score = 0.05
        return {
            "location": buyer["location"],
            "price": buyer["price"],
            "property_type": buyer["property_type"],
            "strategy": buyer["strategy"],
            "repair_profile": buyer["repair_profile"],
            "arv": buyer["arv"],
            "criteria_score": round((geography_score + price_score + property_type_score + strategy_score + repair_profile_score + arv_score) * 100, 2),
        }

    def analyze_buyer_activity(self, buyer: Dict[str, Any]) -> Dict[str, Any]:
        transaction_activity = buyer.get("transaction_activity", 0)
        recent_activity = buyer.get("recent_activity", "")
        activity_score = min(100.0, transaction_activity * 12.5)
        return {
            "transaction_activity": transaction_activity,
            "recent_activity": recent_activity,
            "activity_score": round(activity_score, 2),
        }

    def analyze_buyer_reliability(self, buyer: Dict[str, Any]) -> Dict[str, Any]:
        verified = bool(buyer.get("verified")) and bool(buyer.get("proof_of_funds"))
        reliability_score = float(buyer.get("reliability_score", 0.0))
        return {
            "verified": verified,
            "reliability_score": round(reliability_score, 2),
            "proof_of_funds": buyer.get("proof_of_funds"),
            "evidence_based": verified,
        }

    def gather_opportunities(self, deal_quality_threshold: float = 70.0) -> List[BuyerMatchOpportunity]:
        opportunities: List[BuyerMatchOpportunity] = []
        for buyer in self.search_buyer_database():
            criteria = self.analyze_buyer_criteria(buyer)
            activity = self.analyze_buyer_activity(buyer)
            reliability = self.analyze_buyer_reliability(buyer)
            weighted_score = (
                criteria["criteria_score"] * 0.45
                + activity["activity_score"] * 0.25
                + reliability["reliability_score"] * 0.30
            )
            if weighted_score < deal_quality_threshold:
                continue
            opportunities.append(
                BuyerMatchOpportunity(
                    buyer_id=buyer["buyer_id"],
                    score=round(weighted_score, 2),
                    category="TOP 10 BUYER MATCHES",
                    reason="Buyer aligned to location, price, property type, strategy, and activity profile",
                    location=criteria["location"],
                    price=criteria["price"],
                    property_type=criteria["property_type"],
                    strategy=criteria["strategy"],
                    repair_profile=criteria["repair_profile"],
                    arv=criteria["arv"],
                    historical_behavior=activity["recent_activity"],
                )
            )
        return sorted(opportunities, key=lambda item: item.score, reverse=True)

    def rank_buyers(self, deal_quality_threshold: float = 70.0) -> Dict[str, List[Dict[str, Any]]]:
        opportunities = self.gather_opportunities(deal_quality_threshold=deal_quality_threshold)
        verified = [item for item in opportunities if self.analyze_buyer_reliability(self.search_buyer_database()[0 if item.buyer_id == "buyer-0001" else 1])['verified']]
        high_reliability = [item for item in opportunities if self.analyze_buyer_reliability(self.search_buyer_database()[0 if item.buyer_id == "buyer-0001" else 1])['reliability_score'] >= 80]
        recent = [item for item in opportunities if self.analyze_buyer_activity(self.search_buyer_database()[0 if item.buyer_id == "buyer-0001" else 1])['transaction_activity'] >= 4]

        ranked = BuyerRankedMatch(
            top_10_buyer_matches=opportunities[:10],
            top_verified_buyers=verified[:10],
            top_high_reliability_buyers=high_reliability[:10],
            top_recently_active_buyers=recent[:10],
        )
        return ranked.as_dict()

    def create_outreach_opportunities(self, deal_quality_threshold: float = 70.0) -> List[Dict[str, Any]]:
        opportunities = self.gather_opportunities(deal_quality_threshold=deal_quality_threshold)
        return [item.as_dict() for item in opportunities]

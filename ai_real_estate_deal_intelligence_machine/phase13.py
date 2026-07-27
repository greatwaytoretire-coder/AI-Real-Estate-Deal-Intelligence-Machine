from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DealRoomAccess:
    level: str
    token: str


@dataclass
class DealRoomMetrics:
    views: int = 0
    buyer_interest: int = 0
    questions: int = 0
    offers: int = 0


@dataclass
class DealRoom:
    deal_id: str
    property_summary: str
    location: str
    property_details: Dict[str, Any]
    comps: List[str]
    arv: float
    repairs: float
    underwriting: Dict[str, Any]
    profit_analysis: Dict[str, Any]
    risk_analysis: Dict[str, Any]
    buyer_demand: Dict[str, Any]
    data_confidence: float
    access: DealRoomAccess
    metrics: DealRoomMetrics


class DealRoomAgent:
    """Phase 13 deal room generation foundation."""

    def generate_deal_room(self) -> DealRoom:
        return DealRoom(
            deal_id="deal-001",
            property_summary="Investor-ready property summary",
            location="Austin, TX",
            property_details={"beds": 3, "baths": 2, "sqft": 1450},
            comps=["comp-001", "comp-002"],
            arv=220000,
            repairs=15000,
            underwriting={"maximum_offer": 190000},
            profit_analysis={"roi": 17.5},
            risk_analysis={"risk_score": 72},
            buyer_demand={"buyers": 4},
            data_confidence=0.84,
            access=DealRoomAccess(level="secure", token="token-001"),
            metrics=DealRoomMetrics(),
        )

    def create_update(self, deal_room: DealRoom) -> DealRoom:
        deal_room.metrics.views += 1
        deal_room.metrics.buyer_interest += 1
        return deal_room

from .phase10 import (
BuyerMatchOpportunity,
BuyerRankedMatch,
)

class BuyerMatchingEngine:
    """Buyer matching engine for ranking and outreach opportunities."""
    def __init__(
        self,
        buyer_database: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Initialize the buyer matching engine.

        If a buyer database is supplied, it is used for the current
        simulation or runtime. Otherwise, a small internal mock database
        is used for standalone testing.
        """

        if buyer_database is None:
            buyer_database = [
                {
                    "buyer_id": "buyer-0001",
                    "location": "Austin, TX",
                    "price": "150000-260000",
                    "property_type": "single-family",
                    "strategy": "fix-and-flip",
                    "repair_profile": "light rehab",
                    "arv": "210000-240000",
                    "historical_behavior": (
                        "closed 2 deals in 90 days"
                    ),
                    "verified": True,
                    "reliability_score": 93.0,
                    "recent_activity": (
                        "closed 2 deals in the last 90 days"
                    ),
                    "transaction_activity": 6,
                    "proof_of_funds": (
                        "bank statement snapshot"
                    ),
                },
                {
                    "buyer_id": "buyer-0002",
                    "location": "Dallas, TX",
                    "price": "200000-320000",
                    "property_type": "multi-family",
                    "strategy": "buy-and-hold",
                    "repair_profile": "moderate rehab",
                    "arv": "250000-300000",
                    "historical_behavior": (
                        "active in the last 30 days"
                    ),
                    "verified": False,
                    "reliability_score": 72.0,
                    "recent_activity": (
                        "made 4 offers in the last 30 days"
                    ),
                    "transaction_activity": 4,
                    "proof_of_funds": None,
                },
            ]

        self._buyer_database = list(buyer_database)

        self._buyer_lookup: Dict[str, Dict[str, Any]] = {
            buyer["buyer_id"]: buyer
            for buyer in self._buyer_database
            if buyer.get("buyer_id")
        }

    def search_buyer_database(
        self,
        location: Optional[str] = None,
        price_range: Optional[str] = None,
        property_type: Optional[str] = None,
        strategy: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search the currently active buyer database."""

        candidates = list(self._buyer_database)

        if location:
            location_lower = location.lower()

            candidates = [
                buyer
                for buyer in candidates
                if location_lower
                in str(
                    buyer.get("location", "")
                ).lower()
            ]

        if price_range:
            candidates = [
                buyer
                for buyer in candidates
                if buyer.get("price") == price_range
            ]

        if property_type:
            candidates = [
                buyer
                for buyer in candidates
                if buyer.get("property_type")
                == property_type
            ]

        if strategy:
            candidates = [
                buyer
                for buyer in candidates
                if buyer.get("strategy")
                == strategy
            ]

        return candidates

    def analyze_buyer_criteria(
        self,
        buyer: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze buyer fit criteria safely."""

        geography_score = (
            0.30
            if buyer.get("location")
            else 0.0
        )

        price_score = (
            0.20
            if buyer.get("price")
            else 0.0
        )

        property_type_score = (
            0.20
            if buyer.get("property_type")
            else 0.0
        )

        strategy_score = (
            0.15
            if buyer.get("strategy")
            else 0.0
        )

        repair_profile_score = (
            0.10
            if buyer.get("repair_profile")
            else 0.0
        )

        arv_score = (
            0.05
            if buyer.get("arv")
            else 0.0
        )

        return {
            "location": buyer.get("location"),
            "price": buyer.get("price"),
            "property_type": buyer.get(
                "property_type"
            ),
            "strategy": buyer.get(
                "strategy"
            ),
            "repair_profile": buyer.get(
                "repair_profile"
            ),
            "arv": buyer.get("arv"),
            "criteria_score": round(
                (
                    geography_score
                    + price_score
                    + property_type_score
                    + strategy_score
                    + repair_profile_score
                    + arv_score
                )
                * 100,
                2,
            ),
        }

    def analyze_buyer_activity(
        self,
        buyer: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze buyer activity."""

        transaction_activity = int(
            buyer.get(
                "transaction_activity",
                0,
            )
        )

        recent_activity = buyer.get(
            "recent_activity",
            "",
        )

        activity_score = min(
            100.0,
            transaction_activity * 12.5,
        )

        return {
            "transaction_activity": (
                transaction_activity
            ),
            "recent_activity": (
                recent_activity
            ),
            "activity_score": round(
                activity_score,
                2,
            ),
        }

    def analyze_buyer_reliability(
        self,
        buyer: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze buyer reliability and verification."""

        verified = (
            bool(
                buyer.get(
                    "verified"
                )
            )
            and bool(
                buyer.get(
                    "proof_of_funds"
                )
            )
        )

        reliability_score = float(
            buyer.get(
                "reliability_score",
                0.0,
            )
        )

        return {
            "verified": verified,
            "reliability_score": round(
                reliability_score,
                2,
            ),
            "proof_of_funds": buyer.get(
                "proof_of_funds"
            ),
            "evidence_based": verified,
        }

    def gather_opportunities(
        self,
        deal_quality_threshold: float = 70.0,
    ) -> List[BuyerMatchOpportunity]:
        """Build ranked buyer match opportunities."""

        opportunities: List[
            BuyerMatchOpportunity
        ] = []

        for buyer in self.search_buyer_database():

            criteria = (
                self.analyze_buyer_criteria(
                    buyer
                )
            )

            activity = (
                self.analyze_buyer_activity(
                    buyer
                )
            )

            reliability = (
                self.analyze_buyer_reliability(
                    buyer
                )
            )

            weighted_score = (
                criteria["criteria_score"]
                * 0.45
                + activity["activity_score"]
                * 0.25
                + reliability[
                    "reliability_score"
                ]
                * 0.30
            )

            if (
                weighted_score
                < deal_quality_threshold
            ):
                continue

            opportunities.append(
                BuyerMatchOpportunity(
                    buyer_id=buyer.get(
                        "buyer_id",
                        "",
                    ),
                    score=round(
                        weighted_score,
                        2,
                    ),
                    category=(
                        "TOP 10 BUYER MATCHES"
                    ),
                    reason=(
                        "Buyer aligned to "
                        "available criteria, "
                        "activity, and "
                        "reliability data"
                    ),
                    location=buyer.get(
                        "location",
                        "",
                    ),
                    price=buyer.get(
                        "price",
                        "",
                    ),
                    property_type=buyer.get(
                        "property_type",
                        "",
                    ),
                    strategy=buyer.get(
                        "strategy",
                        "",
                    ),
                    repair_profile=(
                        buyer.get(
                            "repair_profile",
                            "",
                        )
                        or ""
                    ),
                    arv=(
                        buyer.get(
                            "arv",
                            "",
                        )
                        or ""
                    ),
                    historical_behavior=(
                        activity[
                            "recent_activity"
                        ]
                    ),
                )
            )

        return sorted(
            opportunities,
            key=lambda item: item.score,
            reverse=True,
        )

    def rank_buyers(
        self,
        deal_quality_threshold: float = 70.0,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Rank buyers into matching categories."""

        opportunities = (
            self.gather_opportunities(
                deal_quality_threshold=(
                    deal_quality_threshold
                )
            )
        )

        verified: List[
            BuyerMatchOpportunity
        ] = []

        high_reliability: List[
            BuyerMatchOpportunity
        ] = []

        recent: List[
            BuyerMatchOpportunity
        ] = []

        for opportunity in opportunities:

            buyer = self._buyer_lookup.get(
                opportunity.buyer_id
            )

            if buyer is None:
                continue

            reliability = (
                self.analyze_buyer_reliability(
                    buyer
                )
            )

            activity = (
                self.analyze_buyer_activity(
                    buyer
                )
            )

            if reliability["verified"]:
                verified.append(
                    opportunity
                )

            if (
                reliability[
                    "reliability_score"
                ]
                >= 80
            ):
                high_reliability.append(
                    opportunity
                )

            if (
                activity[
                    "transaction_activity"
                ]
                >= 4
            ):
                recent.append(
                    opportunity
                )

        ranked = BuyerRankedMatch(
            top_10_buyer_matches=(
                opportunities[:10]
            ),
            top_verified_buyers=(
                verified[:10]
            ),
            top_high_reliability_buyers=(
                high_reliability[:10]
            ),
            top_recently_active_buyers=(
                recent[:10]
            ),
        )

        return ranked.as_dict()

    def create_outreach_opportunities(
        self,
        deal_quality_threshold: float = 70.0,
    ) -> List[Dict[str, Any]]:
        """Create buyer outreach opportunities."""

        opportunities = (
            self.gather_opportunities(
                deal_quality_threshold=(
                    deal_quality_threshold
                )
            )
        )

        return [
            opportunity.as_dict()
            for opportunity in opportunities
        ]
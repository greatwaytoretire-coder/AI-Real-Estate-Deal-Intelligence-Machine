from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PropertyProfile:
    address: str
    price: float
    property_type: str
    bedrooms: int
    bathrooms: int
    square_footage: int
    year_built: int
    days_on_market: int
    price_change: float = 0.0
    equity_signal: float = 0.0
    distress_signal: float = 0.0
    condition_signal: float = 0.0
    score: float = 0.0

    def __post_init__(self) -> None:
        self.score = round(
            (
                max(0, 100 - self.days_on_market)
                + (self.price / 1000) * 0.08
                + self.equity_signal * 10
                + max(0, 5 - self.distress_signal * 5)
                + self.condition_signal * 10
            )
            / 2,
            2,
        )


@dataclass
class PropertyEvent:
    event_type: str
    payload: Dict[str, Any]
    source: str = "mock"


@dataclass
class DealCandidate:
    property_profile: PropertyProfile
    why_promising: str
    action: str = "schedule_review"


class PropertyDiscoveryAgent:
    """Phase 4 property discovery foundation for new property evaluation."""

    def __init__(self) -> None:
        self._profiles = [
            PropertyProfile(
                address="101 Mock Street",
                price=215000,
                property_type="single_family",
                bedrooms=3,
                bathrooms=2,
                square_footage=1450,
                year_built=2005,
                days_on_market=21,
                price_change=0.04,
                equity_signal=0.72,
                distress_signal=0.22,
                condition_signal=0.68,
            ),
            PropertyProfile(
                address="201 Opportunity Ave",
                price=179000,
                property_type="duplex",
                bedrooms=4,
                bathrooms=2,
                square_footage=1680,
                year_built=1997,
                days_on_market=12,
                price_change=0.02,
                equity_signal=0.64,
                distress_signal=0.19,
                condition_signal=0.55,
            ),
        ]

    def create_property_event(self, profile: PropertyProfile) -> PropertyEvent:
        return PropertyEvent(
            event_type="NEW_PROPERTY_DISCOVERED",
            payload={
                "address": profile.address,
                "price": profile.price,
                "property_type": profile.property_type,
                "score": profile.score,
            },
            source="mock-discovery-agent",
        )

    def deduplicate(self, profile: PropertyProfile) -> bool:
        return profile.address not in {"101 Mock Street"}

    def enrich(self, profile: PropertyProfile) -> PropertyProfile:
        profile.equity_signal = max(profile.equity_signal, 0.5)
        profile.condition_signal = max(profile.condition_signal, 0.5)
        return profile

    def analyze(self, profile: PropertyProfile) -> PropertyProfile:
        profile.score = round(profile.score + 2.0, 2)
        return profile

    def score(self, profile: PropertyProfile) -> float:
        return profile.score

    def determine_follow_up(self, profile: PropertyProfile) -> str:
        return "schedule_review" if profile.score >= 60 else "monitor"

    def find_deal_candidates(self) -> List[DealCandidate]:
        candidates: List[DealCandidate] = []
        for profile in self._profiles:
            enriched = self.enrich(profile)
            analyzed = self.analyze(enriched)
            if self.deduplicate(analyzed) and analyzed.score >= 60:
                candidates.append(
                    DealCandidate(
                        property_profile=analyzed,
                        why_promising="Strong equity and condition signals with low distress",
                        action=self.determine_follow_up(analyzed),
                    )
                )
        return candidates

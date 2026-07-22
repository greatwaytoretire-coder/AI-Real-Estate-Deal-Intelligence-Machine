from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4


@dataclass
class BuyerContactInfo:
    """Stores contact information and communication preferences for a buyer."""

    email: Optional[str] = None
    phone: Optional[str] = None
    preferred_contact_method: str = "email"  # 'email', 'phone', 'sms'
    has_opted_out: bool = False


@dataclass
class BuyerInvestmentCriteria:
    """Defines the specific investment criteria for a buyer."""

    markets: List[str] = field(default_factory=list)
    geographic_preferences: List[str] = field(default_factory=list)  # e.g., ZIP codes, neighborhoods
    property_types: List[str] = field(default_factory=list)
    price_range_min: float = 0.0
    price_range_max: float = 0.0
    investment_strategies: List[str] = field(default_factory=list)
    rehab_tolerance: str = "any"  # 'light', 'moderate', 'heavy', 'any'


@dataclass
class BuyerActivity:
    """Summarizes a buyer's recent transaction activity."""

    deals_closed_last_12m: int = 0
    offers_made_last_90d: int = 0
    last_activity_timestamp: Optional[str] = None


@dataclass
class EnhancedBuyerProfile:
    """
    A comprehensive buyer profile for Phase 34, consolidating identity,
    criteria, activity, and contact information.
    """

    buyer_id: str = field(default_factory=lambda: f"bp_{uuid4()}")
    name: str = "Unnamed Buyer"

    # Data provenance
    data_source: str = "unknown"
    data_freshness_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    confidence_score: float = 0.0

    # Sub-models
    criteria: BuyerInvestmentCriteria = field(default_factory=BuyerInvestmentCriteria)
    activity: BuyerActivity = field(default_factory=BuyerActivity)
    contact_info: BuyerContactInfo = field(default_factory=BuyerContactInfo)

    # Verification
    verification_status: str = "UNVERIFIED"  # UNVERIFIED, PENDING, VERIFIED
    proof_of_funds_verified: bool = False


@dataclass
class BuyerStrategyClassification:
    """Stores the classified strategy for a buyer with a confidence score."""

    strategy: str = "Unknown"
    confidence: float = 0.0
    reasoning: str = "Insufficient data"


class BuyerStrategyClassifier:
    """Classifies a buyer's investment strategy based on their profile."""

    def classify(self, profile: EnhancedBuyerProfile) -> BuyerStrategyClassification:
        """Analyzes a buyer's profile to determine their likely strategy."""
        strategies = profile.criteria.investment_strategies
        prop_types = profile.criteria.property_types
        rehab = profile.criteria.rehab_tolerance

        if "Fix and Flip" in strategies:
            return BuyerStrategyClassification(
                strategy="Fix-and-flip",
                confidence=0.85,
                reasoning="Buyer explicitly lists 'Fix and Flip' as a strategy.",
            )
        if "Buy-and-hold" in strategies:
            return BuyerStrategyClassification(
                strategy="Buy-and-hold",
                confidence=0.80,
                reasoning="Buyer explicitly lists 'Buy-and-hold' as a strategy.",
            )
        if "Multifamily" in prop_types:
            return BuyerStrategyClassification(
                strategy="Multifamily investor",
                confidence=0.75,
                reasoning="Buyer's preferred property types include 'Multifamily'.",
            )
        if rehab == "heavy":
            return BuyerStrategyClassification(
                strategy="Heavy-rehab investor",
                confidence=0.70,
                reasoning="Buyer has a tolerance for 'heavy' rehab projects.",
            )

        return BuyerStrategyClassification()


@dataclass
class BuyerReliabilityScore:
    """Stores the calculated reliability score for a buyer."""

    score: float = 0.0
    reasoning: List[str] = field(default_factory=list)
    is_reliable: bool = False


class BuyerReliabilityScorer:
    """Scores a buyer's reliability based on verifiable evidence."""

    def score(self, profile: EnhancedBuyerProfile) -> BuyerReliabilityScore:
        """Calculates a reliability score from 0 to 100."""
        score = 20.0  # Base score for existing
        reasoning = ["Base score for profile existence."]

        # Score based on verification status
        if profile.verification_status == "VERIFIED":
            score += 30.0
            reasoning.append("+30 points for VERIFIED status.")
        if profile.proof_of_funds_verified:
            score += 20.0
            reasoning.append("+20 points for verified proof of funds.")

        # Score based on activity
        if profile.activity.deals_closed_last_12m > 0:
            activity_bonus = min(20.0, profile.activity.deals_closed_last_12m * 5)
            score += activity_bonus
            reasoning.append(f"+{activity_bonus} points for recent transaction history.")

        # Score based on data source quality
        if profile.data_source in ["user_provided", "crm_import"]:
            score += 10.0
            reasoning.append("+10 points for high-quality data source.")

        final_score = min(100.0, score)

        return BuyerReliabilityScore(
            score=final_score,
            reasoning=reasoning,
            is_reliable=(final_score >= 70.0),
        )


@dataclass
class DealContext:
    """A simplified representation of a deal for matching purposes."""

    deal_id: str
    zip_code: str
    property_type: str
    purchase_price: float
    estimated_rehab_level: str  # 'light', 'moderate', 'heavy'
    investment_strategy: str  # 'Fix-and-flip', 'Buy-and-hold'


@dataclass
class BuyerMatchResult:
    """Stores the result of matching a single buyer to a deal."""

    buyer_profile: EnhancedBuyerProfile
    match_score: float = 0.0
    match_reasons: List[str] = field(default_factory=list)
    mismatch_reasons: List[str] = field(default_factory=list)


class BuyerDealMatcher:
    """Matches deals to buyers based on comprehensive profile criteria."""

    def __init__(self):
        self.reliability_scorer = BuyerReliabilityScorer()

    def match(self, deal: DealContext, buyers: List[EnhancedBuyerProfile]) -> List[BuyerMatchResult]:
        """Finds and ranks the best buyer matches for a given deal."""
        results = []
        for buyer in buyers:
            score = 0.0
            match_reasons = []
            mismatch_reasons = []

            # Geography
            if deal.zip_code in buyer.criteria.geographic_preferences:
                score += 30
                match_reasons.append("Matches preferred ZIP code.")
            else:
                mismatch_reasons.append("Deal is outside preferred ZIP codes.")

            # Price Range
            if buyer.criteria.price_range_min <= deal.purchase_price <= buyer.criteria.price_range_max:
                score += 25
                match_reasons.append("Price is within buyer's range.")
            else:
                mismatch_reasons.append("Price is outside buyer's range.")

            # Investment Strategy
            if deal.investment_strategy in buyer.criteria.investment_strategies:
                score += 20
                match_reasons.append("Matches investment strategy.")

            # Reliability Score
            reliability = self.reliability_scorer.score(buyer)
            score += reliability.score * 0.25  # Reliability acts as a multiplier/boost
            match_reasons.append(f"Reliability score of {reliability.score:.0f} applied.")

            results.append(
                BuyerMatchResult(
                    buyer_profile=buyer, match_score=score, match_reasons=match_reasons, mismatch_reasons=mismatch_reasons
                )
            )

        return sorted(results, key=lambda r: r.match_score, reverse=True)
        )
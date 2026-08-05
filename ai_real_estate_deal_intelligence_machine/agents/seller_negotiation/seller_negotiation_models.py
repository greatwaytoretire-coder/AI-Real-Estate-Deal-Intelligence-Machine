from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class SellerNegotiationDecision:
    """
    Output produced by Seller Negotiation AI Agent.
    """

    property_id: str
    seller_name: str

    motivation_score: float
    distress_score: float
    urgency_level: str

    recommended_strategy: str

    offer_range_low: float
    offer_range_high: float

    reasoning: List[str]
    
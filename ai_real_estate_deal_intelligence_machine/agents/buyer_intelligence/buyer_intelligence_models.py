from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class BuyerIntelligenceDecision:
    """
    Output produced by Buyer Intelligence AI Agent.
    """

    buyer_id: str
    buyer_name: str

    buyer_type: str

    preferred_markets: List[str]
    preferred_property_types: List[str]

    investment_score: float
    deal_match_score: float

    recommendation: str

    reasoning: List[str]
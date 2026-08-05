from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class DispositionRecommendation:
    property_id: str
    address: str
    recommended_strategy: str
    target_buyer_type: str
    estimated_assignment_fee: float
    confidence_score: float
    reasoning: List[str]


@dataclass
class ExitStrategy:
    name: str
    description: str
    ideal_buyer: str
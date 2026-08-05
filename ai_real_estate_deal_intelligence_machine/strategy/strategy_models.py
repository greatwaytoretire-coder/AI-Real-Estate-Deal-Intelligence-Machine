from dataclasses import dataclass
from datetime import datetime


@dataclass
class StrategyRecommendation:
    property_id: str
    strategy: str
    confidence: float
    notes: str
    created_at: datetime
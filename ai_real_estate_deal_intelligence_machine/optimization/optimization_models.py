from dataclasses import dataclass
from datetime import datetime


@dataclass
class OptimizationRecommendation:
    category: str
    recommendation: str
    confidence: float
    created_at: datetime
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DealFeedback:
    deal_id: str
    predicted_profit: float
    actual_profit: float
    accuracy_score: float
    created_at: datetime
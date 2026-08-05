from dataclasses import dataclass
from datetime import datetime


@dataclass
class DealOutcome:
    deal_id: str
    address: str
    outcome: str
    actual_profit: float
    expected_profit: float
    completed_at: datetime


@dataclass
class LearningRecord:
    deal_id: str
    lesson: str
    category: str
    created_at: datetime
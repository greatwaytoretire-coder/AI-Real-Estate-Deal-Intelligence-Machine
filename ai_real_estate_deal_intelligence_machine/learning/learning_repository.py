from datetime import datetime, timezone
from typing import List

from ai_real_estate_deal_intelligence_machine.learning.learning_models import (
    LearningRecord,
)


class LearningRepository:
    """
    Persistent storage layer for learning events.

    Stores:
    - deal outcomes
    - model improvements
    - detected patterns
    """


    def __init__(self):

        self.records: List[LearningRecord] = []



    def save(
        self,
        record: LearningRecord,
    ):

        self.records.append(record)

        return record



    def get_all(self):

        return self.records



    def count(self):

        return len(self.records)
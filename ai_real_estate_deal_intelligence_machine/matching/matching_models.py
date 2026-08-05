from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class BuyerMatch:

    buyer_id: str
    buyer_name: str

    score: float

    recommendation: str

    reasoning: List[str]
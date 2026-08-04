from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class AcquisitionDecision:
    """
    Result produced by the Acquisition AI Agent.
    """

    property_id: str
    address: str

    deal_score: float

    recommendation: str

    reasoning: List[str] = field(default_factory=list)
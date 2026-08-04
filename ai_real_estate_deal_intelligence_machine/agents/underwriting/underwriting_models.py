from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class UnderwritingDecision:
    """
    Financial analysis result produced by the Underwriting AI Agent.
    """

    property_id: str
    address: str

    purchase_price: float
    arv: float

    repair_costs: float
    holding_costs: float

    projected_profit: float
    roi_percentage: float

    recommendation: str

    reasoning: List[str]
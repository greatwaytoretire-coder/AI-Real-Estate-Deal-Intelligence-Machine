from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class DealPackage:

    property_id: str

    address: str

    purchase_price: float

    arv: float

    projected_profit: float

    roi: float

    recommendation: str

    buyer_recommendations: List[str] = field(default_factory=list)

    summary: str = ""
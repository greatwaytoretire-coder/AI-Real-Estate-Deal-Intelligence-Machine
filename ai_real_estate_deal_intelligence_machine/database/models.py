from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class PropertyRecord:
    """
    Stored property information.
    """

    property_id: str
    address: str
    market: str
    property_type: str



@dataclass
class SellerRecord:
    """
    Stored seller intelligence.
    """

    seller_id: str
    owner_name: str
    motivation_score: int
    distress_signals: List[str] = field(
        default_factory=list
    )



@dataclass
class DealRecord:
    """
    Master investment opportunity record.
    """

    deal_id: str

    property_id: str

    seller_id: str

    recommendation: str

    deal_score: float

    projected_profit: float

    roi: float

    risk_level: str

    status: str

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )
    
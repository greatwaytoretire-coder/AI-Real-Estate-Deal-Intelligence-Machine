from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass(slots=True)
class ClosedDealRecord:
    """
    Represents the final outcome of a completed investment.
    """

    deal_id: str
    property_id: str
    purchase_price: float
    projected_profit: float
    actual_profit: float
    projected_roi: float
    actual_roi: float
    status: str
    exit_strategy: str
    notes: str = ""
    closed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ClosedDealTracker:
    """
    Stores completed investment results for future learning.

    This is the entry point for the historical learning system.
    """

    def __init__(self) -> None:
        self._closed_deals: list[ClosedDealRecord] = []

    def record(self, record: ClosedDealRecord) -> ClosedDealRecord:
        """
        Save a completed deal.
        """
        self._closed_deals.append(record)
        return record

    def get_all(self) -> list[ClosedDealRecord]:
        """
        Return every stored closed deal.
        """
        return list(self._closed_deals)

    def count(self) -> int:
        """
        Number of stored closed deals.
        """
        return len(self._closed_deals)

    def latest(self) -> Optional[ClosedDealRecord]:
        """
        Return the most recent completed deal.
        """
        if not self._closed_deals:
            return None

        return self._closed_deals[-1]

    def summary(self) -> Dict[str, Any]:
        """
        Basic portfolio summary.
        """
        if not self._closed_deals:
            return {
                "total_closed": 0,
                "average_profit": 0.0,
                "average_roi": 0.0,
            }

        avg_profit = sum(
            d.actual_profit for d in self._closed_deals
        ) / len(self._closed_deals)

        avg_roi = sum(
            d.actual_roi for d in self._closed_deals
        ) / len(self._closed_deals)

        return {
            "total_closed": len(self._closed_deals),
            "average_profit": round(avg_profit, 2),
            "average_roi": round(avg_roi, 2),
        }
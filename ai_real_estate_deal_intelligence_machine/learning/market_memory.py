from __future__ import annotations

from typing import Any, Dict, List


class MarketMemory:
    """
    Stores historical market intelligence.

    Sprint 4 Part 10:
    Market Intelligence Learning Engine.

    Tracks market-level investment outcomes.
    """

    def __init__(self) -> None:

        self._markets: List[Dict[str, Any]] = []


    def store(
        self,
        market_record: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Store market performance data.
        """

        self._markets.append(
            market_record
        )

        return market_record


    def get_all(self) -> List[Dict[str, Any]]:
        """
        Return all market intelligence.
        """

        return list(
            self._markets
        )


    def find_market(
        self,
        market: str,
    ) -> List[Dict[str, Any]]:
        """
        Find historical records for a market.
        """

        return [
            record
            for record in self._markets
            if record.get("market") == market
        ]


    def count(self) -> int:
        """
        Return number of market records.
        """

        return len(
            self._markets
        )


    def summary(self) -> Dict[str, Any]:
        """
        Return market memory summary.
        """

        return {

            "total_market_records":
                len(self._markets),

            "markets_tracked":
                list(
                    {
                        record.get("market")
                        for record in self._markets
                        if record.get("market")
                    }
                ),

            "status":
                "MARKET_MEMORY_READY",

        }
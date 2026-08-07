from __future__ import annotations

from typing import Any, Dict, Iterable


class MarketPatternDetector:
    """
    Detects investment patterns across markets.

    Sprint 4 Part 10:
    Market Intelligence Learning Engine.

    Converts historical market records into
    actionable market intelligence.
    """

    def analyze(
        self,
        market_records: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Analyze historical market performance.
        """

        records = [
            record
            for record in market_records
            if isinstance(record, dict)
        ]


        if not records:
            return {

                "status":
                    "NO_MARKET_DATA",

                "patterns":
                    [],

                "confidence":
                    0,

            }


        total_markets = len(records)


        successful_markets = [
            record
            for record in records
            if float(
                record.get(
                    "success_rate",
                    0,
                )
            ) >= 70
        ]


        high_profit_markets = [
            record
            for record in records
            if float(
                record.get(
                    "average_profit",
                    0,
                )
            ) >= 50000
        ]


        patterns = []


        if successful_markets:

            patterns.append(
                "Markets with strong historical success rates identified."
            )


        if high_profit_markets:

            patterns.append(
                "Markets producing above-average profits identified."
            )


        confidence = (
            len(successful_markets)
            /
            total_markets
            *
            100
        )


        return {

            "status":
                "MARKET_PATTERNS_DETECTED",

            "markets_analyzed":
                total_markets,

            "successful_markets":
                len(successful_markets),

            "high_profit_markets":
                len(high_profit_markets),

            "patterns":
                patterns,

            "confidence":
                round(
                    confidence,
                    2,
                ),

        }
    
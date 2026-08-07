from __future__ import annotations

from typing import Any, Dict


class MarketConfidenceModel:
    """
    Calculates confidence levels for markets.

    Sprint 4 Part 10:
    Market Intelligence Learning Engine.

    Uses historical market performance signals.
    """

    def evaluate(
        self,
        market_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate market confidence.
        """

        success_rate = float(
            market_data.get(
                "success_rate",
                0,
            )
        )

        average_profit = float(
            market_data.get(
                "average_profit",
                0,
            )
        )


        confidence_score = 0


        if success_rate >= 80:
            confidence_score += 50

        elif success_rate >= 60:
            confidence_score += 30

        else:
            confidence_score += 10



        if average_profit >= 75000:
            confidence_score += 50

        elif average_profit >= 50000:
            confidence_score += 30

        else:
            confidence_score += 10



        if confidence_score >= 80:
            confidence_level = "HIGH"

        elif confidence_score >= 50:
            confidence_level = "MEDIUM"

        else:
            confidence_level = "LOW"



        return {

            "market":
                market_data.get(
                    "market",
                    "UNKNOWN",
                ),

            "confidence_score":
                confidence_score,

            "confidence_level":
                confidence_level,

            "signals":
                {
                    "success_rate":
                        success_rate,

                    "average_profit":
                        average_profit,
                },

            "status":
                "MARKET_CONFIDENCE_EVALUATED",

        }
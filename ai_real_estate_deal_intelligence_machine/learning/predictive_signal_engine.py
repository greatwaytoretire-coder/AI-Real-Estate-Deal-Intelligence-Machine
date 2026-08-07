from __future__ import annotations

from typing import Any, Dict


class PredictiveSignalEngine:
    """
    Combines investment intelligence signals.

    Sprint 4 Part 11:
    Predictive Deal Intelligence.

    Converts multiple intelligence sources into
    a unified predictive score.
    """

    def analyze(
        self,
        signals: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze predictive investment signals.
        """

        deal_score = float(
            signals.get(
                "deal_score",
                0,
            )
        )

        market_confidence = float(
            signals.get(
                "market_confidence",
                0,
            )
        )

        seller_motivation = float(
            signals.get(
                "seller_motivation",
                0,
            )
        )

        buyer_demand = float(
            signals.get(
                "buyer_demand",
                0,
            )
        )

        risk_penalty = float(
            signals.get(
                "risk_penalty",
                0,
            )
        )


        predictive_score = (
            (deal_score * 0.35)
            +
            (market_confidence * 0.25)
            +
            (seller_motivation * 0.20)
            +
            (buyer_demand * 0.20)
            -
            risk_penalty
        )


        predictive_score = max(
            min(
                round(
                    predictive_score,
                    2,
                ),
                100,
            ),
            0,
        )


        if predictive_score >= 80:

            recommendation = "STRONG_BUY"

        elif predictive_score >= 60:

            recommendation = "BUY"

        elif predictive_score >= 40:

            recommendation = "REVIEW"

        else:

            recommendation = "PASS"



        return {

            "predictive_score":
                predictive_score,

            "recommendation":
                recommendation,

            "signals_used":
                {
                    "deal_score":
                        deal_score,

                    "market_confidence":
                        market_confidence,

                    "seller_motivation":
                        seller_motivation,

                    "buyer_demand":
                        buyer_demand,

                    "risk_penalty":
                        risk_penalty,
                },

            "status":
                "PREDICTIVE_SIGNALS_ANALYZED",

        }
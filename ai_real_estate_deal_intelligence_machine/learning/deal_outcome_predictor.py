from __future__ import annotations

from typing import Any, Dict


class DealOutcomePredictor:
    """
    Predicts likely deal outcomes.

    Sprint 4 Part 11:
    Predictive Deal Intelligence.

    Uses learned intelligence signals to estimate
    future deal performance.
    """

    def predict(
        self,
        deal_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Predict investment outcome.
        """

        deal_score = float(
            deal_data.get(
                "deal_score",
                0,
            )
        )

        market_confidence = float(
            deal_data.get(
                "market_confidence",
                0,
            )
        )

        profit_margin = float(
            deal_data.get(
                "profit_margin",
                0,
            )
        )

        risk_level = str(
            deal_data.get(
                "risk_level",
                "UNKNOWN",
            )
        )


        success_probability = (
            deal_score * 0.5
            +
            market_confidence * 0.3
            +
            profit_margin * 0.2
        )


        success_probability = min(
            round(
                success_probability,
                2,
            ),
            100,
        )


        if success_probability >= 80:
            confidence = "HIGH"

        elif success_probability >= 60:
            confidence = "MEDIUM"

        else:
            confidence = "LOW"



        if success_probability >= 75:
            recommendation = "PROCEED"

        elif success_probability >= 50:
            recommendation = "REVIEW"

        else:
            recommendation = "AVOID"



        return {

            "deal_id":
                deal_data.get(
                    "deal_id",
                    "UNKNOWN",
                ),

            "success_probability":
                success_probability,

            "predicted_outcome":
                recommendation,

            "confidence":
                confidence,

            "risk_level":
                risk_level,

            "signals":
                {
                    "deal_score":
                        deal_score,

                    "market_confidence":
                        market_confidence,

                    "profit_margin":
                        profit_margin,
                },

            "status":
                "OUTCOME_PREDICTED",

        }
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable


class RetrainingEngine:
    """
    Converts closed-deal learning results into adaptive strategy
    recommendations.

    Sprint 4 Part 8:
    Closed Deal Learning.

    This component does not retrain an ML model directly. Instead,
    it translates observed investment outcomes into controlled
    strategy adjustments that can be consumed by the adaptive
    intelligence layer.
    """

    MINIMUM_SAMPLE_SIZE = 3

    def retrain(
        self,
        outcomes: Iterable[Dict[str, Any]],
        statistics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze historical outcomes and produce strategy adjustments.

        The engine remains conservative when historical sample size
        is small.
        """

        records = [
            outcome
            for outcome in outcomes
            if isinstance(outcome, dict)
        ]

        total_deals = int(
            statistics.get(
                "total_deals",
                len(records),
            )
        )

        success_rate = float(
            statistics.get(
                "success_rate",
                0.0,
            )
        )

        average_profit = float(
            statistics.get(
                "average_profit",
                0.0,
            )
        )

        recommendations: list[str] = []
        adjustments: Dict[str, Any] = {}

        if total_deals < self.MINIMUM_SAMPLE_SIZE:
            recommendations.append(
                "Collect more closed-deal outcomes before making "
                "major strategy adjustments."
            )

            adjustments["strategy_confidence"] = "INSUFFICIENT_DATA"

        else:
            if success_rate >= 80:
                recommendations.append(
                    "Historical success rate is strong; maintain "
                    "current acquisition strategy."
                )

                adjustments["strategy_confidence"] = "HIGH"

            elif success_rate >= 60:
                recommendations.append(
                    "Historical results are moderately successful; "
                    "continue monitoring deal selection."
                )

                adjustments["strategy_confidence"] = "MEDIUM"

            else:
                recommendations.append(
                    "Historical success rate is weak; increase "
                    "deal-selection caution."
                )

                adjustments["strategy_confidence"] = "LOW"

            if average_profit > 0:
                recommendations.append(
                    "Positive average realized profit supports "
                    "continued evaluation of similar opportunities."
                )

                adjustments["profit_direction"] = "POSITIVE"

            elif average_profit < 0:
                recommendations.append(
                    "Negative average realized profit indicates "
                    "that underwriting assumptions should be reviewed."
                )

                adjustments["profit_direction"] = "NEGATIVE"

            else:
                recommendations.append(
                    "Average realized profit is approximately "
                    "break-even."
                )

                adjustments["profit_direction"] = "NEUTRAL"

        return {
            "retraining_status": "COMPLETE",
            "sample_size": total_deals,
            "success_rate": round(
                success_rate,
                2,
            ),
            "average_profit": round(
                average_profit,
                2,
            ),
            "adjustments": adjustments,
            "recommendations": recommendations,
            "retrained_at": datetime.now(
                timezone.utc
            ),
        }
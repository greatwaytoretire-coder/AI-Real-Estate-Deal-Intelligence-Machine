from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


class StrategyOptimizer:
    """
    Optimizes investment strategy recommendations
    using confidence signals and historical patterns.

    Sprint 4 Part 9:
    Learning Intelligence Integration.

    Maintains compatibility with the existing
    AdaptiveEngine while adding historical pattern learning.
    """

    def optimize(
        self,
        confidence_data: Dict[str, Any],
        detected_patterns: List[Any],
    ) -> Dict[str, Any]:

        recommendations = []

        confidence_score = float(
            confidence_data.get(
                "confidence_score",
                0,
            )
        )

        confidence_adjustment = 0

        if confidence_score >= 80:

            recommendations.append(
                "Increase weighting of historically successful acquisition signals."
            )

        elif confidence_score >= 50:

            recommendations.append(
                "Maintain current scoring model while monitoring additional outcomes."
            )

        else:

            recommendations.append(
                "Collect more deal outcomes before making significant strategy changes."
            )


        successful_patterns = 0
        total_profit = 0.0


        for pattern in detected_patterns:

            if isinstance(pattern, dict):

                successful_patterns += float(
                    pattern.get(
                        "success_rate",
                        0,
                    )
                )

                total_profit += float(
                    pattern.get(
                        "average_profit",
                        0,
                    )
                )


        if detected_patterns:

            average_success = (
                successful_patterns /
                len(detected_patterns)
            )

            average_profit = (
                total_profit /
                len(detected_patterns)
            )


            if average_success >= 80:

                confidence_adjustment = 20

                recommendations.append(
                    "Historical patterns strongly support current acquisition strategy."
                )

            elif average_success >= 60:

                confidence_adjustment = 10

                recommendations.append(
                    "Historical patterns moderately support current acquisition strategy."
                )

            else:

                confidence_adjustment = -10

                recommendations.append(
                    "Historical patterns indicate increased acquisition caution."
                )


            if average_profit > 0:

                recommendations.append(
                    "Positive historical profits support similar future opportunities."
                )


        else:

            average_success = 0
            average_profit = 0

            recommendations.append(
                "No historical patterns available yet."
            )


        return {

            "optimization_status":
                "COMPLETE",

            "confidence_score":
                confidence_score,

            "confidence_adjustment":
                confidence_adjustment,

            "average_pattern_success":
                round(
                    average_success,
                    2,
                ),

            "average_pattern_profit":
                round(
                    average_profit,
                    2,
                ),

            "recommendations":
                recommendations,

            "patterns_used":
                detected_patterns,

            "optimized_at":
                datetime.now(
                    timezone.utc
                ),

        }
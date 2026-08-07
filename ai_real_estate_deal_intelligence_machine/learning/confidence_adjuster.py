from __future__ import annotations

from typing import Any, Dict


class ConfidenceAdjuster:
    """
    Adjusts investment confidence using historical learning data.

    Sprint 4 Part 9:
    Learning Intelligence Integration.

    Combines current deal confidence with historical
    performance patterns.
    """

    def adjust(
        self,
        current_confidence: float,
        strategy_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Apply historical intelligence adjustments.
        """

        adjustment = float(
            strategy_result.get(
                "confidence_adjustment",
                0,
            )
        )

        adjusted_confidence = (
            current_confidence +
            adjustment
        )

        adjusted_confidence = max(
            0,
            min(
                adjusted_confidence,
                100,
            ),
        )

        if adjusted_confidence >= 80:

            confidence_level = "HIGH"

        elif adjusted_confidence >= 50:

            confidence_level = "MEDIUM"

        else:

            confidence_level = "LOW"


        return {

            "original_confidence":
                current_confidence,

            "adjustment":
                adjustment,

            "adjusted_confidence":
                round(
                    adjusted_confidence,
                    2,
                ),

            "confidence_level":
                confidence_level,

            "status":
                "CONFIDENCE_ADJUSTED",

        }
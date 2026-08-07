from __future__ import annotations

from typing import Any, Dict


class OutcomeClassifier:
    """
    Classifies completed investment outcomes based on actual
    financial performance.

    Sprint 4 Part 8:
    Closed Deal Learning.
    """

    EXCELLENT_PROFIT = 50000.0
    PROFITABLE_THRESHOLD = 0.0
    BREAK_EVEN_TOLERANCE = 1000.0

    def classify(
        self,
        actual_profit: float,
        actual_roi: float,
    ) -> Dict[str, Any]:
        """
        Classify a closed deal using actual profit and ROI.

        Categories:

        EXCELLENT
            Strong realized profit.

        PROFITABLE
            Positive realized profit.

        BREAK_EVEN
            Result is approximately zero.

        LOSS
            Negative realized profit.
        """

        actual_profit = float(actual_profit)
        actual_roi = float(actual_roi)

        if actual_profit >= self.EXCELLENT_PROFIT:
            category = "EXCELLENT"
            success = True
            lesson = (
                "Deal produced exceptional realized profit."
            )

        elif actual_profit > self.BREAK_EVEN_TOLERANCE:
            category = "PROFITABLE"
            success = True
            lesson = (
                "Deal produced positive realized profit."
            )

        elif abs(actual_profit) <= self.BREAK_EVEN_TOLERANCE:
            category = "BREAK_EVEN"
            success = False
            lesson = (
                "Deal approximately broke even and produced "
                "limited realized profit."
            )

        else:
            category = "LOSS"
            success = False
            lesson = (
                "Deal produced a realized financial loss."
            )

        return {
            "category": category,
            "success": success,
            "actual_profit": round(actual_profit, 2),
            "actual_roi": round(actual_roi, 2),
            "lesson": lesson,
            "status": "OUTCOME_CLASSIFIED",
        }
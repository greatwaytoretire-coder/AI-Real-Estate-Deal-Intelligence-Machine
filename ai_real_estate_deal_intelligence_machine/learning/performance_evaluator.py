from __future__ import annotations

from typing import Any, Dict


class PerformanceEvaluator:
    """
    Evaluates actual closed-deal performance against the original
    investment projections.

    Sprint 4 Part 8:
    Closed Deal Learning.
    """

    def evaluate(
        self,
        projected_profit: float,
        actual_profit: float,
        projected_roi: float,
        actual_roi: float,
    ) -> Dict[str, Any]:
        """
        Compare projected investment performance with actual results.
        """

        projected_profit = float(projected_profit)
        actual_profit = float(actual_profit)
        projected_roi = float(projected_roi)
        actual_roi = float(actual_roi)

        profit_variance = actual_profit - projected_profit
        roi_variance = actual_roi - projected_roi

        if projected_profit != 0:
            profit_accuracy = (
                actual_profit / projected_profit
            ) * 100
        else:
            profit_accuracy = 0.0

        if projected_roi != 0:
            roi_accuracy = (
                actual_roi / projected_roi
            ) * 100
        else:
            roi_accuracy = 0.0

        return {
            "projected_profit": round(projected_profit, 2),
            "actual_profit": round(actual_profit, 2),
            "profit_variance": round(profit_variance, 2),
            "projected_roi": round(projected_roi, 2),
            "actual_roi": round(actual_roi, 2),
            "roi_variance": round(roi_variance, 2),
            "profit_accuracy": round(profit_accuracy, 2),
            "roi_accuracy": round(roi_accuracy, 2),
            "status": "PERFORMANCE_EVALUATED",
        }
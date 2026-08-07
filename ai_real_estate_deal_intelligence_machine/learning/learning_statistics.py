from __future__ import annotations

from typing import Any, Dict, Iterable


class LearningStatistics:
    """
    Calculates portfolio-level statistics from closed deal outcomes.

    Sprint 4 Part 8:
    Closed Deal Learning.
    """

    def calculate(
        self,
        outcomes: Iterable[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate aggregate learning statistics.

        Expected outcome fields:

            actual_profit
            actual_roi
            success
            category

        Missing or invalid records are ignored safely.
        """

        records = []

        for outcome in outcomes:
            if not isinstance(outcome, dict):
                continue

            try:
                actual_profit = float(
                    outcome.get("actual_profit", 0.0)
                )

                actual_roi = float(
                    outcome.get("actual_roi", 0.0)
                )

                success = bool(
                    outcome.get("success", False)
                )

                category = str(
                    outcome.get(
                        "category",
                        "UNKNOWN",
                    )
                )

            except (TypeError, ValueError):
                continue

            records.append(
                {
                    "actual_profit": actual_profit,
                    "actual_roi": actual_roi,
                    "success": success,
                    "category": category,
                }
            )

        total_deals = len(records)

        if total_deals == 0:
            return {
                "total_deals": 0,
                "successful_deals": 0,
                "failed_deals": 0,
                "success_rate": 0.0,
                "average_profit": 0.0,
                "average_roi": 0.0,
                "total_profit": 0.0,
                "best_profit": 0.0,
                "worst_profit": 0.0,
                "categories": {},
                "status": "NO_CLOSED_DEALS",
            }

        successful_deals = sum(
            1
            for record in records
            if record["success"]
        )

        failed_deals = (
            total_deals - successful_deals
        )

        total_profit = sum(
            record["actual_profit"]
            for record in records
        )

        average_profit = (
            total_profit / total_deals
        )

        average_roi = (
            sum(
                record["actual_roi"]
                for record in records
            )
            / total_deals
        )

        best_profit = max(
            record["actual_profit"]
            for record in records
        )

        worst_profit = min(
            record["actual_profit"]
            for record in records
        )

        categories: Dict[str, int] = {}

        for record in records:
            category = record["category"]

            categories[category] = (
                categories.get(category, 0) + 1
            )

        success_rate = (
            successful_deals / total_deals
        ) * 100

        return {
            "total_deals": total_deals,
            "successful_deals": successful_deals,
            "failed_deals": failed_deals,
            "success_rate": round(
                success_rate,
                2,
            ),
            "average_profit": round(
                average_profit,
                2,
            ),
            "average_roi": round(
                average_roi,
                2,
            ),
            "total_profit": round(
                total_profit,
                2,
            ),
            "best_profit": round(
                best_profit,
                2,
            ),
            "worst_profit": round(
                worst_profit,
                2,
            ),
            "categories": categories,
            "status": "STATISTICS_CALCULATED",
        }
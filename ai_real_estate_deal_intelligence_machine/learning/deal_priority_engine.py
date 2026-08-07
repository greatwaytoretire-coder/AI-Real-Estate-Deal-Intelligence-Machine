from __future__ import annotations

from typing import Any, Dict, List


class DealPriorityEngine:
    """
    Converts ranked deals into actionable acquisition priorities.

    Sprint 4 Part 13:
    Autonomous Deal Ranking Intelligence.
    """

    def prioritize(
        self,
        ranked_deals: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Assign acquisition priority levels.

        Priority considers:

        Ranking score
        Recommendation
        Risk level
        """

        prioritized = []

        for deal in ranked_deals:

            ranking_score = float(
                deal.get(
                    "ranking_score",
                    0,
                )
            )

            risk_level = deal.get(
                "risk_level",
                "MEDIUM",
            )

            if (
                ranking_score >= 85
                and risk_level == "LOW"
            ):
                priority = "ACQUIRE_NOW"

            elif ranking_score >= 70:
                priority = "ANALYZE_NEXT"

            elif ranking_score >= 50:
                priority = "WATCH"

            else:
                priority = "IGNORE"


            prioritized.append(
                {
                    "deal_id": deal.get(
                        "deal_id"
                    ),

                    "ranking_score": (
                        ranking_score
                    ),

                    "priority_action": (
                        priority
                    ),

                    "risk_level": (
                        risk_level
                    ),
                }
            )


        prioritized.sort(
            key=lambda x: x[
                "ranking_score"
            ],
            reverse=True,
        )


        return {
            "priority_queue": prioritized,

            "highest_priority": (
                prioritized[0]
                if prioritized
                else None
            ),

            "status":
                "PRIORITY_QUEUE_CREATED",
        }
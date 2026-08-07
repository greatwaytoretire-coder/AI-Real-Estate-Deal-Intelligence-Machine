from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List


class FollowUpScheduler:
    """
    Creates automated follow-up schedules.

    Sprint 4 Part 17:

    Communication Plan
            |
            v
    Follow-Up Timing
            |
            v
    Scheduled Pipeline Actions
    """

    def schedule(
        self,
        communication_plan: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate follow-up schedule.
        """

        deal_id = communication_plan.get(
            "deal_id",
            "UNKNOWN",
        )

        decision = communication_plan.get(
            "decision",
            "MONITOR",
        )

        now = datetime.now(
            timezone.utc
        )


        follow_ups: List[Dict[str, Any]] = []


        if decision == "ACQUIRE":

            follow_ups.extend(
                [
                    {
                        "action":
                            "Initial seller contact",
                        "scheduled_for":
                            now,
                        "priority":
                            "HIGH",
                    },
                    {
                        "action":
                            "Negotiation follow-up",
                        "scheduled_for":
                            now + timedelta(days=2),
                        "priority":
                            "HIGH",
                    },
                    {
                        "action":
                            "Contract status review",
                        "scheduled_for":
                            now + timedelta(days=7),
                        "priority":
                            "MEDIUM",
                    },
                ]
            )


        elif decision == "MONITOR":

            follow_ups.extend(
                [
                    {
                        "action":
                            "Seller motivation review",
                        "scheduled_for":
                            now + timedelta(days=14),
                        "priority":
                            "MEDIUM",
                    },
                    {
                        "action":
                            "Market signal reassessment",
                        "scheduled_for":
                            now + timedelta(days=30),
                        "priority":
                            "LOW",
                    },
                ]
            )


        else:

            follow_ups.append(
                {
                    "action":
                        "Archive opportunity",
                    "scheduled_for":
                        now,
                    "priority":
                        "LOW",
                }
            )


        return {

            "deal_id":
                deal_id,

            "decision":
                decision,

            "follow_up_schedule":
                follow_ups,

            "scheduled_actions":
                len(follow_ups),

            "status":
                "FOLLOW_UP_SCHEDULE_CREATED",

        }
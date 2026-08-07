from __future__ import annotations

from typing import Any, Dict, List


class SellerCommunicationPlanner:
    """
    Creates seller communication strategies.

    Sprint 4 Part 17:

    Acquisition Decision
            |
            v
    Seller Communication
            |
            v
    Contact Execution Plan
    """

    def generate_plan(
        self,
        deal_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate seller communication actions.
        """

        deal_id = deal_data.get(
            "deal_id",
            "UNKNOWN",
        )

        decision = deal_data.get(
            "decision",
            "MONITOR",
        )

        seller_motivation = float(
            deal_data.get(
                "seller_motivation",
                50,
            )
        )


        actions: List[str] = []


        if decision == "ACQUIRE":

            if seller_motivation >= 80:

                communication_style = (
                    "HIGH_MOTIVATION_FAST_RESPONSE"
                )

                actions.extend(
                    [
                        "Contact seller immediately.",
                        "Present acquisition offer.",
                        "Emphasize fast closing capability.",
                    ]
                )


            else:

                communication_style = (
                    "RELATIONSHIP_BUILDING"
                )

                actions.extend(
                    [
                        "Schedule seller conversation.",
                        "Identify seller goals.",
                        "Build trust before negotiation.",
                    ]
                )


        elif decision == "MONITOR":

            communication_style = (
                "FOLLOW_UP_NURTURE"
            )

            actions.extend(
                [
                    "Schedule future seller follow-up.",
                    "Monitor motivation changes.",
                    "Maintain communication history.",
                ]
            )


        else:

            communication_style = (
                "NO_CONTACT"
            )

            actions.append(
                "Archive seller communication."
            )


        return {

            "deal_id":
                deal_id,

            "decision":
                decision,

            "seller_motivation":
                seller_motivation,

            "communication_style":
                communication_style,

            "actions":
                actions,

            "action_count":
                len(actions),

            "status":
                "SELLER_COMMUNICATION_PLAN_CREATED",

        }
from __future__ import annotations

from typing import Any, Dict, List


class NegotiationStrategyEngine:
    """
    Generates seller negotiation strategies.

    Sprint 4 Part 16:

    Acquisition Workflow
            |
            v
    Negotiation Strategy
            |
            v
    Seller Execution Plan
    """

    def generate_strategy(
        self,
        deal_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create negotiation recommendations
        based on deal intelligence.
        """

        deal_id = deal_data.get(
            "deal_id",
            "UNKNOWN",
        )

        seller_motivation = float(
            deal_data.get(
                "seller_motivation",
                50,
            )
        )

        risk_level = str(
            deal_data.get(
                "risk_level",
                "MEDIUM",
            )
        ).upper()


        tactics: List[str] = []


        if seller_motivation >= 80:

            tactics.extend(
                [
                    "Prioritize fast offer presentation.",
                    "Emphasize certainty of closing.",
                    "Use flexible closing terms.",
                ]
            )

            negotiation_style = (
                "MOTIVATED_SELLER_APPROACH"
            )


        elif seller_motivation >= 50:

            tactics.extend(
                [
                    "Build seller relationship.",
                    "Identify seller priorities.",
                    "Negotiate based on property value.",
                ]
            )

            negotiation_style = (
                "RELATIONSHIP_BASED_NEGOTIATION"
            )


        else:

            tactics.extend(
                [
                    "Avoid aggressive pricing pressure.",
                    "Continue seller nurturing.",
                    "Monitor motivation changes.",
                ]
            )

            negotiation_style = (
                "LONG_TERM_FOLLOW_UP"
            )


        if risk_level == "HIGH":

            tactics.append(
                "Include additional risk protections in agreement."
            )


        return {

            "deal_id": deal_id,

            "seller_motivation":
                seller_motivation,

            "risk_level":
                risk_level,

            "negotiation_style":
                negotiation_style,

            "recommended_tactics":
                tactics,

            "tactic_count":
                len(tactics),

            "status":
                "NEGOTIATION_STRATEGY_CREATED",

        }
from __future__ import annotations

from typing import Any, Dict


class SellerResponseAnalyzer:
    """
    Analyzes seller responses after acquisition outreach.

    Sprint 4 Part 18:

    Seller Communication
            |
            v
    Response Analysis
            |
            v
    Learning Signals
    """

    def analyze(
        self,
        response_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Analyze seller response signals.
        """

        seller_response = response_data.get(
            "seller_response",
            "UNKNOWN",
        )

        motivation = float(
            response_data.get(
                "seller_motivation",
                0,
            )
        )


        if seller_response == "INTERESTED":

            response_score = 90
            conversion_signal = "HIGH"

        elif seller_response == "NEGOTIATING":

            response_score = 75
            conversion_signal = "MEDIUM"

        elif seller_response == "NO_RESPONSE":

            response_score = 20
            conversion_signal = "LOW"

        else:

            response_score = 50
            conversion_signal = "UNKNOWN"



        adjusted_score = round(
            (
                response_score * 0.7
                +
                motivation * 0.3
            ),
            2,
        )


        return {

            "deal_id":
                response_data.get(
                    "deal_id",
                    "UNKNOWN",
                ),

            "seller_response":
                seller_response,

            "seller_motivation":
                motivation,

            "response_score":
                response_score,

            "adjusted_response_score":
                adjusted_score,

            "conversion_signal":
                conversion_signal,

            "status":
                "SELLER_RESPONSE_ANALYZED",

        }
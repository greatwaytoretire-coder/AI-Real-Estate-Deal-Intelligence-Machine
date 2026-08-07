from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


class NegotiationOutcomeTracker:
    """
    Tracks negotiation outcomes.

    Sprint 4 Part 18:

    Seller Response
            |
            v
    Negotiation Result
            |
            v
    Learning Signals
    """

    def __init__(self) -> None:

        self.negotiations: List[Dict[str, Any]] = []


    def record_negotiation(
        self,
        negotiation_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Record negotiation outcome.
        """

        result = negotiation_data.get(
            "negotiation_result",
            "UNKNOWN",
        )


        if result == "ACCEPTED":

            negotiation_score = 100
            status = "SUCCESSFUL_NEGOTIATION"


        elif result == "COUNTER_OFFER":

            negotiation_score = 70
            status = "ACTIVE_NEGOTIATION"


        elif result == "REJECTED":

            negotiation_score = 20
            status = "FAILED_NEGOTIATION"


        else:

            negotiation_score = 50
            status = "UNKNOWN_NEGOTIATION"



        record = {

            "deal_id":
                negotiation_data.get(
                    "deal_id",
                    "UNKNOWN",
                ),

            "offer_amount":
                negotiation_data.get(
                    "offer_amount",
                    0,
                ),

            "seller_counter_offer":
                negotiation_data.get(
                    "seller_counter_offer",
                    0,
                ),

            "negotiation_result":
                result,

            "negotiation_score":
                negotiation_score,

            "status":
                status,

            "recorded_at":
                datetime.now(
                    timezone.utc
                ),

        }


        self.negotiations.append(
            record
        )


        return record



    def get_negotiations(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Return negotiation history.
        """

        return self.negotiations
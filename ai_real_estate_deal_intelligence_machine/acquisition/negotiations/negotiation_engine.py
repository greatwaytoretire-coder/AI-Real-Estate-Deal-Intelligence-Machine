from dataclasses import dataclass
from enum import Enum


class NegotiationStage(Enum):
    INITIAL_OFFER = "Initial Offer"
    COUNTER_OFFER_RECEIVED = "Counter Offer Received"
    NEGOTIATING = "Negotiating"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"


@dataclass
class NegotiationAnalysis:
    deal_id: str

    current_offer: float

    seller_counter_offer: float

    arv: float

    negotiation_stage: NegotiationStage

    recommended_offer: float

    acceptance_probability: float

    reasoning: list[str]


class NegotiationEngine:
    """
    Analyzes seller negotiations and recommends acquisition actions.

    Flow:

    Acquisition Offer
            |
            v
    Seller Response
            |
            v
    Negotiation Analysis
            |
            v
    Recommended Action
    """


    def __init__(self):

        self.negotiations = []


    def analyze_negotiation(
        self,
        deal_id: str,
        current_offer: float,
        seller_counter_offer: float,
        arv: float,
    ) -> NegotiationAnalysis:

        reasoning = []

        offer_gap = seller_counter_offer - current_offer

        if seller_counter_offer <= current_offer:

            stage = NegotiationStage.ACCEPTED

            recommended_offer = current_offer

            probability = 95

            reasoning.append(
                "Seller price expectation is within current offer."
            )


        elif offer_gap <= arv * 0.05:

            stage = NegotiationStage.NEGOTIATING

            recommended_offer = (
                current_offer + (offer_gap * 0.50)
            )

            probability = 75

            reasoning.append(
                "Seller counter offer is close to acquisition target."
            )


        else:

            stage = NegotiationStage.COUNTER_OFFER_RECEIVED

            recommended_offer = (
                current_offer + (offer_gap * 0.25)
            )

            probability = 55

            reasoning.append(
                "Seller counter offer exceeds preferred negotiation range."
            )


        if recommended_offer < arv * 0.75:

            reasoning.append(
                "Recommended offer maintains strong margin."
            )

        else:

            reasoning.append(
                "Margin should be reviewed before increasing offer."
            )


        analysis = NegotiationAnalysis(
            deal_id=deal_id,
            current_offer=current_offer,
            seller_counter_offer=seller_counter_offer,
            arv=arv,
            negotiation_stage=stage,
            recommended_offer=round(
                recommended_offer,
                2,
            ),
            acceptance_probability=probability,
            reasoning=reasoning,
        )


        self.negotiations.append(
            analysis
        )


        return analysis


    def get_negotiations(
        self,
    ) -> list[NegotiationAnalysis]:

        return self.negotiations
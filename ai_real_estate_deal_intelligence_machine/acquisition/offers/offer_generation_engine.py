from dataclasses import dataclass


@dataclass
class AcquisitionOffer:

    property_id: str

    arv: float

    repair_cost: float

    recommended_offer: float

    confidence_score: float

    reasoning: list[str]


class OfferGenerationEngine:
    """
    Generates acquisition offer recommendations.

    Flow:

    Acquisition Deal
          |
          v
    Deal Analysis
          |
          v
    Offer Calculation
          |
          v
    Recommended Purchase Offer
    """


    def __init__(self):

        self.default_profit_margin = 0.20


    def calculate_offer(
        self,
        property_id: str,
        arv: float,
        repair_cost: float,
        desired_profit_margin: float | None = None,
    ) -> AcquisitionOffer:


        if desired_profit_margin is None:

            desired_profit_margin = self.default_profit_margin


        reasoning = []


        investor_profit_requirement = (
            arv * desired_profit_margin
        )


        recommended_offer = (
            arv
            -
            repair_cost
            -
            investor_profit_requirement
        )


        if recommended_offer < 0:

            recommended_offer = 0


        confidence_score = 50.0


        if arv > 0:

            confidence_score += 20

            reasoning.append(
                "After repair value identified."
            )


        if repair_cost < arv * 0.30:

            confidence_score += 15

            reasoning.append(
                "Repair costs are within acceptable investment range."
            )

        else:

            reasoning.append(
                "High repair costs require additional review."
            )


        if recommended_offer > 0:

            confidence_score += 15

            reasoning.append(
                "Offer preserves investor profit requirements."
            )


        return AcquisitionOffer(

            property_id=property_id,

            arv=arv,

            repair_cost=repair_cost,

            recommended_offer=round(
                recommended_offer,
                2,
            ),

            confidence_score=min(
                confidence_score,
                100,
            ),

            reasoning=reasoning,

        )
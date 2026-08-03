from dataclasses import dataclass
from enum import Enum



class AcquisitionDealStatus(Enum):

    NEW = "New"

    ANALYSIS_COMPLETE = "Analysis Complete"

    OFFER_READY = "Offer Ready"

    OFFER_SENT = "Offer Sent"

    UNDER_CONTRACT = "Under Contract"

    CLOSED = "Closed"



@dataclass
class AcquisitionDeal:

    deal_id: str

    seller_id: str

    property_address: str

    estimated_value: float

    repair_cost: float

    recommended_offer: float

    status: AcquisitionDealStatus

    notes: list[str]



class AcquisitionDealManager:
    """
    Manages acquisition opportunities.

    Flow:

    Seller Lead
          |
          v
    Deal Creation
          |
          v
    Offer Analysis
          |
          v
    Acquisition Decision
    """



    def __init__(self):

        self.deals = [

            AcquisitionDeal(
                deal_id="DEAL-001",
                seller_id="SELLER-001",
                property_address="123 Main Street",
                estimated_value=275000,
                repair_cost=35000,
                recommended_offer=165000,
                status=AcquisitionDealStatus.ANALYSIS_COMPLETE,
                notes=[
                    "Motivated seller opportunity.",
                    "Ready for acquisition review.",
                ],
            ),

        ]



    def get_deals(
        self,
    ) -> list[AcquisitionDeal]:

        return self.deals



    def calculate_offer_readiness(
        self,
        deal: AcquisitionDeal,
    ) -> float:

        equity_margin = (
            deal.estimated_value
            -
            deal.repair_cost
            -
            deal.recommended_offer
        )


        score = 50.0


        if equity_margin > 50000:

            score += 30


        if deal.status == AcquisitionDealStatus.ANALYSIS_COMPLETE:

            score += 20


        return score



    def advance_status(
        self,
        deal_id: str,
        new_status: AcquisitionDealStatus,
        note: str,
    ) -> AcquisitionDeal:


        for deal in self.deals:

            if deal.deal_id == deal_id:

                deal.status = new_status

                deal.notes.append(note)

                return deal



        raise ValueError(
            "Acquisition deal not found."
        )
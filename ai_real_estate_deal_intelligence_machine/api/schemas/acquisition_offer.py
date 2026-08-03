from pydantic import BaseModel


class AcquisitionOfferRequest(BaseModel):

    property_id: str

    arv: float

    repair_cost: float

    desired_profit_margin: float | None = None



class AcquisitionOfferResponse(BaseModel):

    property_id: str

    arv: float

    repair_cost: float

    recommended_offer: float

    confidence_score: float

    reasoning: list[str]
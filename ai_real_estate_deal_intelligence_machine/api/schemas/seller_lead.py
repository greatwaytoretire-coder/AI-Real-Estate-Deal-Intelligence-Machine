from pydantic import BaseModel


class SellerLeadRequest(BaseModel):

    market: str

    property_address: str

    estimated_value: float

    motivation_score: float

    distress_signals: list[str]



class SellerLeadResponse(BaseModel):

    seller_id: str

    owner_name: str

    priority_score: float

    recommendation: str

    reasoning: list[str]
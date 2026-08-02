from pydantic import BaseModel


class BuyerMatchRequest(BaseModel):

    property_id: str

    purchase_price: float

    estimated_value: float

    repair_cost: float



class BuyerMatchResponse(BaseModel):

    buyer_id: str

    buyer_name: str

    match_score: float

    reasoning: list[str]
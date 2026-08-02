from pydantic import BaseModel


class RecommendationRequest(BaseModel):

    property_id: str

    purchase_price: float

    estimated_value: float

    repair_cost: float
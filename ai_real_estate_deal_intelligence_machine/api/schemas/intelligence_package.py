from pydantic import BaseModel


class IntelligencePackageRequest(BaseModel):

    property_id: str

    purchase_price: float

    estimated_value: float

    repair_cost: float



class IntelligencePackageResponse(BaseModel):

    property_id: str

    deal_score: float

    recommendation: str

    priority: str

    reasoning: list[str]

    status: str
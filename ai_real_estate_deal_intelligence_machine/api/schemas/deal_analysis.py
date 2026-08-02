from pydantic import BaseModel


class DealAnalysisRequest(BaseModel):

    property_id: str

    purchase_price: float

    estimated_value: float

    repair_cost: float


class DealAnalysisResponse(BaseModel):

    property_id: str

    projected_profit: float

    deal_score: float

    investment_grade: str

    recommended_action: str

    executive_summary: str

    strengths: list[str]

    risks: list[str]
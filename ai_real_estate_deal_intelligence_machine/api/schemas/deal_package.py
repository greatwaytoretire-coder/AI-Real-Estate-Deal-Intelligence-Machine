from pydantic import BaseModel


class DealPackageRequest(BaseModel):
    property_id: str
    purchase_price: float
    estimated_value: float
    repair_cost: float


class DealPackageResponse(BaseModel):
    property_id: str
    executive_summary: str
    recommendation: str
    deal_score: float
    projected_profit: float
    profit_margin: float
    risk_level: str
    status: str
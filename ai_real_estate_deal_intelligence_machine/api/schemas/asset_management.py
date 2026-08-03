from pydantic import BaseModel


class AssetCreateRequest(BaseModel):

    asset_id: str
    property_address: str
    acquisition_price: float
    closing_date: str
    strategy: str


class AssetResponse(BaseModel):

    asset_id: str
    property_address: str
    acquisition_price: float
    closing_date: str
    strategy: str
    status: str
    monthly_income: float
    monthly_expenses: float
    notes: list[str]


class AssetPerformanceResponse(BaseModel):

    asset_id: str
    monthly_income: float
    monthly_expenses: float
    monthly_cash_flow: float
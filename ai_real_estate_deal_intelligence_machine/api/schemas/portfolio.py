from pydantic import BaseModel


class PortfolioCreateRequest(BaseModel):

    portfolio_id: str
    owner_id: str



class PortfolioAssetRequest(BaseModel):

    asset_id: str



class PortfolioFinancialUpdateRequest(BaseModel):

    total_value: float
    total_equity: float
    monthly_income: float
    monthly_expenses: float



class PortfolioStatusUpdateRequest(BaseModel):

    status: str
    note: str



class PortfolioResponse(BaseModel):

    portfolio_id: str
    owner_id: str

    assets: list[str]

    total_value: float
    total_equity: float

    monthly_income: float
    monthly_expenses: float

    status: str

    notes: list[str]
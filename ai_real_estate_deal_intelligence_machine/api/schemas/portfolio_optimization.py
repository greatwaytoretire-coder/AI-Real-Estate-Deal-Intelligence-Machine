from pydantic import BaseModel


class PortfolioOptimizationRequest(BaseModel):

    portfolio_id: str
    total_value: float
    equity: float
    annual_income: float
    annual_expenses: float


class PortfolioOptimizationResponse(BaseModel):

    portfolio_id: str

    health_score: int

    roi: float

    cash_on_cash_return: float

    cap_rate: float

    risk_score: int

    recommendation: str

    reasons: list[str]
from fastapi import APIRouter

from ai_real_estate_deal_intelligence_machine.portfolio.portfolio_management_engine import (
    PortfolioManagementEngine,
    PortfolioStatus,
)

from ai_real_estate_deal_intelligence_machine.api.schemas.portfolio import (
    PortfolioCreateRequest,
    PortfolioAssetRequest,
    PortfolioFinancialUpdateRequest,
    PortfolioStatusUpdateRequest,
)


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio Intelligence"],
)


engine = PortfolioManagementEngine()



@router.post("")
def create_portfolio(
    request: PortfolioCreateRequest,
):

    return engine.create_portfolio(
        portfolio_id=request.portfolio_id,
        owner_id=request.owner_id,
    )



@router.get("")
def get_portfolios():

    return engine.get_portfolios()



@router.post("/{portfolio_id}/assets")
def add_asset(
    portfolio_id: str,
    request: PortfolioAssetRequest,
):

    return engine.add_asset(
        portfolio_id,
        request.asset_id,
    )



@router.put("/{portfolio_id}/financials")
def update_financials(
    portfolio_id: str,
    request: PortfolioFinancialUpdateRequest,
):

    return engine.update_financials(
        portfolio_id,
        request.total_value,
        request.total_equity,
        request.monthly_income,
        request.monthly_expenses,
    )



@router.get("/{portfolio_id}/performance")
def portfolio_performance(
    portfolio_id: str,
):

    return engine.calculate_performance(
        portfolio_id
    )



@router.put("/{portfolio_id}/status")
def update_status(
    portfolio_id: str,
    request: PortfolioStatusUpdateRequest,
):

    return engine.update_status(
        portfolio_id,
        PortfolioStatus(request.status),
        request.note,
    )
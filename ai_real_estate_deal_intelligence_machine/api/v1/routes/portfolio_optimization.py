from fastapi import APIRouter, HTTPException

from ai_real_estate_deal_intelligence_machine.api.schemas.portfolio_optimization import (
    PortfolioOptimizationRequest,
)
from ai_real_estate_deal_intelligence_machine.portfolio.portfolio_optimizer import (
    PortfolioOptimizer,
)

router = APIRouter(
    prefix="/portfolio-optimization",
    tags=["Portfolio Optimization"],
)

optimizer = PortfolioOptimizer()


@router.post("")
def optimize_portfolio(request: PortfolioOptimizationRequest):
    try:
        return optimizer.analyze_portfolio(
            portfolio_id=request.portfolio_id,
            total_value=request.total_value,
            equity=request.equity,
            annual_income=request.annual_income,
            annual_expenses=request.annual_expenses,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
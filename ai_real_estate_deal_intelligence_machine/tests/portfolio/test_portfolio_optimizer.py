from ai_real_estate_deal_intelligence_machine.portfolio.portfolio_optimizer import (
    PortfolioOptimizer,
    InvestmentRecommendation,
)



def test_portfolio_health_analysis():

    optimizer = PortfolioOptimizer()


    result = optimizer.analyze_portfolio(
        portfolio_id="PORT-001",
        total_value=500000,
        equity=200000,
        annual_income=60000,
        annual_expenses=20000,
    )


    assert result.health_score == 100

    assert result.recommendation == (
        InvestmentRecommendation.HOLD
    )



def test_negative_cash_flow_risk():

    optimizer = PortfolioOptimizer()


    result = optimizer.analyze_portfolio(
        portfolio_id="PORT-002",
        total_value=500000,
        equity=50000,
        annual_income=30000,
        annual_expenses=40000,
    )


    assert result.health_score < 100

    assert result.recommendation != (
        InvestmentRecommendation.HOLD
    )



def test_invalid_value():

    optimizer = PortfolioOptimizer()


    try:

        optimizer.analyze_portfolio(
            portfolio_id="INVALID",
            total_value=0,
            equity=0,
            annual_income=10000,
            annual_expenses=1000,
        )


        assert False


    except ValueError as error:

        assert str(error) == (
            "Portfolio value must be greater than zero."
        )
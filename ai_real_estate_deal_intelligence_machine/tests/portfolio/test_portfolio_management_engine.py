from ai_real_estate_deal_intelligence_machine.portfolio.portfolio_management_engine import (
    PortfolioManagementEngine,
    PortfolioStatus,
)



def test_create_portfolio():

    engine = PortfolioManagementEngine()

    portfolio = engine.create_portfolio(
        portfolio_id="PORT-001",
        owner_id="OWNER-001",
    )

    assert portfolio.portfolio_id == "PORT-001"
    assert portfolio.status == PortfolioStatus.ACTIVE



def test_add_asset():

    engine = PortfolioManagementEngine()

    engine.create_portfolio(
        "PORT-002",
        "OWNER-002",
    )

    portfolio = engine.add_asset(
        "PORT-002",
        "ASSET-001",
    )

    assert "ASSET-001" in portfolio.assets



def test_portfolio_performance():

    engine = PortfolioManagementEngine()

    engine.create_portfolio(
        "PORT-003",
        "OWNER-003",
    )

    engine.update_financials(
        "PORT-003",
        1000000,
        300000,
        8000,
        3000,
    )

    result = engine.calculate_performance(
        "PORT-003"
    )

    assert result["cash_flow"] == 5000



def test_missing_portfolio():

    engine = PortfolioManagementEngine()

    try:

        engine.add_asset(
            "INVALID",
            "ASSET",
        )

        assert False

    except ValueError as error:

        assert str(error) == "Portfolio not found."
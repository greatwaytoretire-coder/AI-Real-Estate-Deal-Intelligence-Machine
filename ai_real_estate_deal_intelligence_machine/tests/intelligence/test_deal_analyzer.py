from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
)


def test_mao_calculation():

    analyzer = DealAnalyzer()

    mao = analyzer.calculate_mao(
        250000,
        35000,
    )

    assert mao == 140000


def test_profit_calculation():

    analyzer = DealAnalyzer()

    profit = analyzer.calculate_profit(
        250000,
        150000,
        35000,
    )

    assert profit == 65000


def test_deal_analysis():

    analyzer = DealAnalyzer()

    result = analyzer.analyze(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )

    assert result.projected_profit == 65000
    assert result.investment_grade == "STRONG"
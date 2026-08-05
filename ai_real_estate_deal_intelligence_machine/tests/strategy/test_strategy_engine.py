from ai_real_estate_deal_intelligence_machine.strategy.strategy_engine import (
    StrategyEngine,
)


def test_strategy_engine_returns_strategy():

    engine = StrategyEngine()

    recommendation = engine.recommend_strategy(
        property_id="PROP-100",
        roi=0.30,
        repair_cost_ratio=0.10,
    )

    assert recommendation.strategy == "FIX_AND_FLIP"
    assert recommendation.confidence > 0
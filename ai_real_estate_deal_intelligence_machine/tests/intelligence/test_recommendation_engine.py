from ai_real_estate_deal_intelligence_machine.intelligence.deal_analyzer import (
    DealAnalyzer,
)

from ai_real_estate_deal_intelligence_machine.intelligence.recommendation_engine import (
    RecommendationEngine,
)


def test_high_value_deal_recommendation():

    analyzer = DealAnalyzer()

    analysis = analyzer.analyze(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )

    engine = RecommendationEngine()

    recommendation = engine.generate(
        analysis
    )

    assert recommendation.property_id == "PROP-001"

    assert recommendation.recommendation in [
        "ACQUIRE",
        "PURSUE",
    ]

    assert recommendation.priority in [
        "HIGH",
        "MEDIUM",
    ]

    assert len(
        recommendation.reasoning
    ) > 0


def test_low_value_deal_recommendation():

    analyzer = DealAnalyzer()

    analysis = analyzer.analyze(
        property_id="PROP-002",
        purchase_price=220000,
        estimated_value=230000,
        repair_cost=20000,
    )

    engine = RecommendationEngine()

    recommendation = engine.generate(
        analysis
    )

    assert recommendation.recommendation in [
        "NEGOTIATE",
        "PASS",
    ]

    assert len(
        recommendation.reasoning
    ) > 0
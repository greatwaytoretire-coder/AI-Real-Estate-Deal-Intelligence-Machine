from ai_real_estate_deal_intelligence_machine.disposition.disposition_engine import (
    DispositionEngine,
)


def test_disposition_engine_recommends_wholesale():

    engine = DispositionEngine()

    result = engine.recommend(
        property_data={
            "property_id": "PROP-100",
            "address": "123 Main Street",
        },
        deal_data={
            "purchase_price": 200000,
            "arv": 300000,
            "repair_costs": 20000,
        },
        buyer_data={
            "buyers": 5,
        },
    )

    assert result.recommended_strategy == "WHOLESALE_ASSIGNMENT"
    assert result.estimated_assignment_fee > 0
    assert len(result.reasoning) > 0


def test_disposition_engine_recommends_hold():

    engine = DispositionEngine()

    result = engine.recommend(
        property_data={
            "property_id": "PROP-200",
            "address": "456 Oak Street",
        },
        deal_data={
            "purchase_price": 300000,
            "arv": 310000,
            "repair_costs": 5000,
        },
        buyer_data={},
    )

    assert result.recommended_strategy == "BUY_AND_HOLD"
from ai_real_estate_deal_intelligence_machine.buyers.buyer_intelligence_engine import (
    BuyerIntelligenceEngine,
)


def test_buyer_intelligence_engine():

    engine = BuyerIntelligenceEngine()


    matches = engine.find_matches(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )


    assert len(matches) > 0


    match = matches[0]


    assert match.buyer_id is not None

    assert match.buyer_name is not None

    assert match.match_score >= 0

    assert match.reasoning is not None
from ai_real_estate_deal_intelligence_machine.acquisition.offers.offer_generation_engine import (
    OfferGenerationEngine,
)


def test_generate_acquisition_offer():

    engine = OfferGenerationEngine()


    result = engine.calculate_offer(
        property_id="PROPERTY-001",
        arv=300000,
        repair_cost=50000,
    )


    assert result.property_id == "PROPERTY-001"

    assert result.arv == 300000

    assert result.repair_cost == 50000

    assert result.recommended_offer == 190000

    assert result.confidence_score > 0

    assert len(result.reasoning) > 0



def test_offer_respects_custom_profit_margin():

    engine = OfferGenerationEngine()


    result = engine.calculate_offer(
        property_id="PROPERTY-002",
        arv=500000,
        repair_cost=100000,
        desired_profit_margin=0.25,
    )


    assert result.recommended_offer == 275000

    assert result.confidence_score <= 100
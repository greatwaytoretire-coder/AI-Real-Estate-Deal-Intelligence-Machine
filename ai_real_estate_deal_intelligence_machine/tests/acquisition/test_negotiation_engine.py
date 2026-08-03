from ai_real_estate_deal_intelligence_machine.acquisition.negotiations.negotiation_engine import (
    NegotiationEngine,
    NegotiationStage,
)


def test_negotiation_acceptance_analysis():

    engine = NegotiationEngine()

    result = engine.analyze_negotiation(
        deal_id="DEAL-001",
        current_offer=200000,
        seller_counter_offer=200000,
        arv=350000,
    )

    assert result.negotiation_stage == NegotiationStage.ACCEPTED
    assert result.acceptance_probability == 95


def test_negotiation_close_counter_offer():

    engine = NegotiationEngine()

    result = engine.analyze_negotiation(
        deal_id="DEAL-002",
        current_offer=200000,
        seller_counter_offer=215000,
        arv=350000,
    )

    assert result.negotiation_stage == NegotiationStage.NEGOTIATING
    assert result.recommended_offer > 200000


def test_negotiation_large_gap():

    engine = NegotiationEngine()

    result = engine.analyze_negotiation(
        deal_id="DEAL-003",
        current_offer=200000,
        seller_counter_offer=300000,
        arv=350000,
    )

    assert result.negotiation_stage == NegotiationStage.COUNTER_OFFER_RECEIVED
    assert result.acceptance_probability == 55


def test_margin_reasoning():

    engine = NegotiationEngine()

    result = engine.analyze_negotiation(
        deal_id="DEAL-004",
        current_offer=150000,
        seller_counter_offer=160000,
        arv=400000,
    )

    assert len(result.reasoning) >= 2


def test_engine_storage():

    engine = NegotiationEngine()

    engine.analyze_negotiation(
        deal_id="DEAL-005",
        current_offer=180000,
        seller_counter_offer=185000,
        arv=350000,
    )

    assert len(engine.get_negotiations()) == 1
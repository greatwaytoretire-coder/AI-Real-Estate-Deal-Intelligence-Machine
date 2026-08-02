from ai_real_estate_deal_intelligence_machine.intelligence.deal_intelligence_coordinator import (
    DealIntelligenceCoordinator,
)



def test_deal_intelligence_coordinator():

    coordinator = DealIntelligenceCoordinator()


    result = coordinator.analyze(
        property_id="PROP-001",
        purchase_price=150000,
        estimated_value=250000,
        repair_cost=35000,
    )


    assert result.property_id == "PROP-001"

    assert result.status == "COMPLETED"

    assert result.deal_score > 0

    assert result.recommendation in [
        "ACQUIRE",
        "PURSUE",
        "NEGOTIATE",
        "PASS",
    ]
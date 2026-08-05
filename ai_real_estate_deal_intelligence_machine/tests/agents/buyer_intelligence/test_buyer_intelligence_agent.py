from ai_real_estate_deal_intelligence_machine.agents.buyer_intelligence.buyer_intelligence_agent import (
    BuyerIntelligenceAgent,
)


def test_buyer_intelligence_returns_high_priority_match():

    agent = BuyerIntelligenceAgent()

    decision = agent.analyze(
        buyer_data={
            "buyer_name": "Phoenix Capital",
            "buyer_type": "Cash Investor",
            "preferred_markets": [
                "Phoenix"
            ],
            "preferred_property_types": [
                "Single Family"
            ],
            "investment_score": 90,
        },
        deal_data={
            "market": "Phoenix",
            "property_type": "Single Family",
        },
    )

    assert decision.recommendation == (
        "HIGH_PRIORITY_BUYER"
    )


def test_buyer_intelligence_returns_reasoning():

    agent = BuyerIntelligenceAgent()

    decision = agent.analyze(
        buyer_data={
            "buyer_name": "Test Buyer",
            "investment_score": 40,
        },
        deal_data={
            "market": "Dallas",
            "property_type": "Condo",
        },
    )

    assert len(decision.reasoning) > 0
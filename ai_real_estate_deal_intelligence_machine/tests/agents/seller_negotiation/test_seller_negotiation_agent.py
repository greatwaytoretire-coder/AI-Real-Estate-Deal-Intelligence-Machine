from ai_real_estate_deal_intelligence_machine.agents.seller_negotiation.seller_negotiation_agent import (
    SellerNegotiationAgent,
)


def test_seller_negotiation_agent_returns_strategy():

    agent = SellerNegotiationAgent()

    decision = agent.analyze(
        seller_data={
            "seller_name": "John Smith",
            "motivaton_score": 85,
            "motivation_score": 85,
            "distress_score": 80,
        },
        property_data={
            "estimated_value": 300000,
        },
    )

    assert decision.recommended_strategy == (
        "AGGRESSIVE_NEGOTIATION"
    )


def test_seller_negotiation_agent_returns_reasoning():

    agent = SellerNegotiationAgent()

    decision = agent.analyze(
        seller_data={
            "seller_name": "Jane Doe",
            "motivation_score": 40,
            "distress_score": 20,
        },
        property_data={
            "estimated_value": 250000,
        },
    )

    assert len(decision.reasoning) > 0
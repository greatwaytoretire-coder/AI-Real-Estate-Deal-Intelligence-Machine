from ai_real_estate_deal_intelligence_machine.agents.acquisition.acquisition_agent import (
    AcquisitionAgent,
)


def test_acquisition_agent_identifies_opportunity():

    agent = AcquisitionAgent()

    decision = agent.analyze(
        property_data={
            "address": "500 Intelligence Avenue",
            "price": 325000,
        },
        market_data={
            "market_score": 91,
        },
        valuation_data={
            "estimated_value": 400000,
        },
    )

    assert decision.recommendation == "PURSUE"

    assert decision.deal_score >= 70


def test_acquisition_agent_returns_reasoning():

    agent = AcquisitionAgent()

    decision = agent.analyze(
        property_data={
            "address": "123 Main Street",
            "price": 300000,
        },
        market_data={
            "market_score": 50,
        },
        valuation_data={
            "estimated_value": 310000,
        },
    )

    assert len(decision.reasoning) > 0
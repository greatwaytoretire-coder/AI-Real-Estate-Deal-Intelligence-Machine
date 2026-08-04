from ai_real_estate_deal_intelligence_machine.agents.underwriting.underwriting_agent import (
    UnderwritingAgent,
)


def test_underwriting_agent_approves_profitable_deal():

    agent = UnderwritingAgent()

    decision = agent.analyze(
        property_data={
            "address": "500 Intelligence Avenue",
            "price": 250000,
        },
        valuation_data={
            "estimated_value": 400000,
        },
        expense_data={
            "repair_costs": 30000,
            "holding_costs": 10000,
        },
    )

    assert decision.recommendation == "APPROVE"

    assert decision.projected_profit == 110000

    assert decision.roi_percentage > 15


def test_underwriting_agent_returns_financial_reasoning():

    agent = UnderwritingAgent()

    decision = agent.analyze(
        property_data={
            "address": "123 Main Street",
            "price": 300000,
        },
        valuation_data={
            "estimated_value": 310000,
        },
        expense_data={
            "repair_costs": 10000,
            "holding_costs": 5000,
        },
    )

    assert len(decision.reasoning) > 0
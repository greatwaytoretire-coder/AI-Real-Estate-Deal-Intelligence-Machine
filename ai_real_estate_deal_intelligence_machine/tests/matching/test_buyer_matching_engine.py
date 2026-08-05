from ai_real_estate_deal_intelligence_machine.matching.buyer_matching_engine import (
    BuyerMatchingEngine,
)


def test_best_buyer_is_ranked_first():

    engine = BuyerMatchingEngine()

    buyers = [
        {
            "buyer_id": "1",
            "buyer_name": "Investor A",
            "preferred_markets": ["Phoenix"],
            "preferred_property_types": ["Single Family"],
            "investment_score": 90,
        },
        {
            "buyer_id": "2",
            "buyer_name": "Investor B",
            "preferred_markets": ["Dallas"],
            "preferred_property_types": ["Condo"],
            "investment_score": 50,
        },
    ]

    deal = {
        "market": "Phoenix",
        "property_type": "Single Family",
    }

    matches = engine.match(
        buyers,
        deal,
    )

    assert matches[0].buyer_name == "Investor A"


def test_matching_returns_reasoning():

    engine = BuyerMatchingEngine()

    buyers = [
        {
            "buyer_id": "1",
            "buyer_name": "Investor",
            "preferred_markets": [],
            "preferred_property_types": [],
            "investment_score": 20,
        }
    ]

    deal = {
        "market": "Miami",
        "property_type": "Condo",
    }

    matches = engine.match(
        buyers,
        deal,
    )

    assert len(matches[0].reasoning) > 0
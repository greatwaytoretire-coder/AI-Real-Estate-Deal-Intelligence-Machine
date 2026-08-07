from ai_real_estate_deal_intelligence_machine.learning.market_learning_engine import (
    MarketLearningEngine,
)


def main():

    print("=" * 70)
    print("SPRINT 4 PART 10 INTEGRATION TEST")
    print("MARKET LEARNING INTELLIGENCE")
    print("=" * 70)


    market_data = [

        {
            "market": "Detroit",
            "property_type": "single_family",
            "success_rate": 85,
            "average_profit": 72000,
        },

        {
            "market": "Cleveland",
            "property_type": "single_family",
            "success_rate": 70,
            "average_profit": 55000,
        },

        {
            "market": "Chicago",
            "property_type": "multi_family",
            "success_rate": 45,
            "average_profit": 25000,
        },

    ]


    print(
        "\nSTEP 1 - Running Market Learning Engine"
    )


    engine = MarketLearningEngine()


    result = engine.learn(
        market_data
    )


    print(result)


    print(
        "\nSTEP 2 - Market Recommendations"
    )


    for recommendation in result["recommendations"]:

        print(
            recommendation
        )


    print()


    print("=" * 70)
    print(
        "SPRINT 4 PART 10 INTEGRATION TEST COMPLETE"
    )
    print("=" * 70)



if __name__ == "__main__":

    main()
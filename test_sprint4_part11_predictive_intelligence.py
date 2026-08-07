from ai_real_estate_deal_intelligence_machine.learning.predictive_intelligence_engine import (
    PredictiveIntelligenceEngine,
)


def main():

    print("=" * 70)
    print("SPRINT 4 PART 11 INTEGRATION TEST")
    print("PREDICTIVE DEAL INTELLIGENCE")
    print("=" * 70)


    engine = PredictiveIntelligenceEngine()


    print(
        "\nSTEP 1 - Loading Investment Intelligence Signals"
    )


    deal_data = {

        "deal_id":
            "DEAL-001",

        "deal_score":
            90,

        "market_confidence":
            80,

        "seller_motivation":
            95,

        "buyer_demand":
            90,

        "profit_margin":
            60,

        "risk_level":
            "LOW",

        "risk_penalty":
            5,

    }


    print(deal_data)



    print(
        "\nSTEP 2 - Running Predictive Intelligence"
    )


    result = engine.analyze(
        deal_data
    )


    print(result)



    print(
        "\nSTEP 3 - Prediction Result"
    )


    print(
        result["prediction"]
    )



    print(
        "\nSTEP 4 - Investment Recommendation"
    )


    print(
        result["recommendation"]
    )



    print()
    print("=" * 70)
    print(
        "SPRINT 4 PART 11 INTEGRATION TEST COMPLETE"
    )
    print("=" * 70)



if __name__ == "__main__":
    main()
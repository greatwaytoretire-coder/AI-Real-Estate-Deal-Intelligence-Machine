from ai_real_estate_deal_intelligence_machine.learning.acquisition_decision_integration import (
    AcquisitionDecisionIntegration,
)


def main():

    print("=" * 70)
    print("SPRINT 4 PART 15 INTEGRATION TEST")
    print("ACQUISITION DECISION INTELLIGENCE")
    print("=" * 70)


    print("\nSTEP 1 - Loading Deal Recommendations")


    recommendations = [

        {
            "deal_id": "DEAL-001",
            "recommendation": "PURSUE",
            "recommendation_score": 81.6,
            "confidence_score": 91.1,
            "confidence_level": "HIGH",
            "risk_level": "LOW",
        },

        {
            "deal_id": "DEAL-002",
            "recommendation": "PASS",
            "recommendation_score": 52.1,
            "confidence_score": 56.55,
            "confidence_level": "LOW",
            "risk_level": "MEDIUM",
        },

        {
            "deal_id": "DEAL-003",
            "recommendation": "PASS",
            "recommendation_score": 9.5,
            "confidence_score": 8.75,
            "confidence_level": "LOW",
            "risk_level": "HIGH",
        },

    ]


    print(recommendations)


    print("\nSTEP 2 - Running Acquisition Decision Intelligence")


    engine = AcquisitionDecisionIntegration()

    result = engine.evaluate(
        recommendations
    )


    print(result)


    print("\nSTEP 3 - Acquisition Candidates")


    print(
        result[
            "acquisition_candidates"
        ]
    )


    print("\nSTEP 4 - Validation")


    assert (
        result["status"]
        ==
        "ACQUISITION_DECISION_INTEGRATION_COMPLETE"
    )


    assert (
        len(
            result["evaluations"]
        )
        == 3
    )


    assert (
        result[
            "acquisition_candidates"
        ][0]["decision"]["decision"]
        ==
        "ACQUIRE"
    )


    print("Validation successful")


    print("\n" + "=" * 70)
    print("SPRINT 4 PART 15 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
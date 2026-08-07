"""
Sprint 4 Part 18 Integration Test
Outcome Learning Intelligence

Validates:
- Acquisition outcome analysis
- Learning signal generation
- Feedback loop creation
"""

from ai_real_estate_deal_intelligence_machine.learning.outcome_learning_integration import (
    OutcomeLearningIntegration,
)


def main():

    print("=" * 70)
    print("SPRINT 4 PART 18 INTEGRATION TEST")
    print("OUTCOME LEARNING INTELLIGENCE")
    print("=" * 70)


    print("\nSTEP 1 - Loading Completed Acquisition Outcomes")


    outcomes = [

        {
            "deal_id": "DEAL-001",
            "success": True,
            "profit_result": "POSITIVE",
            "negotiation_result": "SUCCESS",
        },

        {
            "deal_id": "DEAL-002",
            "success": False,
            "profit_result": "NEGATIVE",
            "negotiation_result": "FAILED",
        },

        {
            "deal_id": "DEAL-003",
            "success": True,
            "profit_result": "POSITIVE",
            "negotiation_result": "SUCCESS",
        },

    ]


    print(outcomes)



    print("\nSTEP 2 - Running Outcome Learning Intelligence")


    engine = OutcomeLearningIntegration()


    analysis = engine.analyze_outcomes(
        outcomes
    )


    learning_signal = engine.generate_learning_signal(
        analysis
    )


    result = {

        "analysis": analysis,

        "learning_signal": learning_signal,

        "status":
            "OUTCOME_LEARNING_COMPLETE",

    }


    print(result)



    print("\nSTEP 3 - Learning Insights")


    print(
        learning_signal
    )



    print("\nSTEP 4 - Validation")


    assert result["status"] == "OUTCOME_LEARNING_COMPLETE"

    assert analysis["total_outcomes"] == 3

    assert analysis["successful_outcomes"] == 2

    assert analysis["failed_outcomes"] == 1

    assert "learning_adjustment" in analysis

    assert learning_signal["status"] == "LEARNING_SIGNAL_GENERATED"


    print("Validation successful")



    print("\n" + "=" * 70)
    print("SPRINT 4 PART 18 INTEGRATION TEST COMPLETE")
    print("=" * 70)



if __name__ == "__main__":
    main()
from ai_real_estate_deal_intelligence_machine.learning.execution_automation_integration import (
    ExecutionAutomationIntegration,
)


def main():

    print("=" * 70)
    print("SPRINT 4 PART 17 INTEGRATION TEST")
    print("EXECUTION AUTOMATION INTELLIGENCE")
    print("=" * 70)


    acquisition_workflows = [

        {
            "decision": {
                "deal_id":
                    "DEAL-001",

                "decision":
                    "ACQUIRE",
            },

            "strategy": {

                "strategy":
                    "DIRECT_ACQUISITION",

                "seller_motivation":
                    90,

            },
        },


        {
            "decision": {

                "deal_id":
                    "DEAL-002",

                "decision":
                    "MONITOR",

            },

            "strategy": {

                "strategy":
                    "MARKET_MONITORING",

                "seller_motivation":
                    60,

            },
        },


        {
            "decision": {

                "deal_id":
                    "DEAL-003",

                "decision":
                    "PASS",

            },

            "strategy": {

                "strategy":
                    "NO_ACQUISITION_ACTION",

                "seller_motivation":
                    20,

            },
        },

    ]


    print("\nSTEP 1 - Loading Acquisition Workflows")

    print(
        acquisition_workflows
    )


    print(
        "\nSTEP 2 - Running Execution Automation"
    )


    engine = (
        ExecutionAutomationIntegration()
    )


    result = engine.execute(
        acquisition_workflows
    )


    print(
        result
    )


    print(
        "\nSTEP 3 - Acquisition Ready Plans"
    )


    print(
        result[
            "acquisition_ready"
        ]
    )


    print(
        "\nSTEP 4 - Validation"
    )


    assert (
        result["status"]
        ==
        "EXECUTION_AUTOMATION_COMPLETE"
    )


    assert (
        len(
            result[
                "execution_plans"
            ]
        )
        ==
        3
    )


    assert (
        len(
            result[
                "acquisition_ready"
            ]
        )
        ==
        1
    )


    print(
        "Validation successful"
    )


    print("=" * 70)
    print(
        "SPRINT 4 PART 17 INTEGRATION TEST COMPLETE"
    )
    print("=" * 70)



if __name__ == "__main__":
    main()
from ai_real_estate_deal_intelligence_machine.learning.acquisition_workflow_integration import (
    AcquisitionWorkflowIntegration,
)


print("=" * 70)
print("SPRINT 4 PART 16 INTEGRATION TEST")
print("ACQUISITION WORKFLOW INTELLIGENCE")
print("=" * 70)


acquisition_candidates = [

    {
        "decision": {
            "deal_id": "DEAL-001",
            "decision": "ACQUIRE",
            "risk_level": "LOW",
            "recommendation": "PURSUE",
            "confidence_level": "HIGH",
        },
        "strategy": {
            "strategy": "DIRECT_ACQUISITION",
            "seller_motivation": 90,
        },
    },


    {
        "decision": {
            "deal_id": "DEAL-002",
            "decision": "MONITOR",
            "risk_level": "MEDIUM",
            "recommendation": "PASS",
            "confidence_level": "LOW",
        },
        "strategy": {
            "strategy": "MARKET_MONITORING",
            "seller_motivation": 60,
        },
    },

]


print()
print("STEP 1 - Loading Acquisition Candidates")

print(acquisition_candidates)


print()
print("STEP 2 - Running Acquisition Workflow Intelligence")


engine = AcquisitionWorkflowIntegration()


result = engine.execute(
    acquisition_candidates
)


print(result)


print()
print("STEP 3 - Acquisition Ready Deals")


print(
    result["acquisition_ready"]
)


print()
print("STEP 4 - Validation")


assert (
    result["status"]
    ==
    "ACQUISITION_WORKFLOW_INTEGRATION_COMPLETE"
)


assert (
    len(
        result["execution_plans"]
    )
    ==
    2
)


assert (
    len(
        result["acquisition_ready"]
    )
    ==
    1
)


print(
    "Validation successful"
)


print()
print("=" * 70)
print("SPRINT 4 PART 16 INTEGRATION TEST COMPLETE")
print("=" * 70)
from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_progress_integration import (
    AcquisitionProgressIntegration,
)


def main() -> None:
    print("=" * 70)
    print("SPRINT 4 PART 25 INTEGRATION TEST")
    print("ACQUISITION PROGRESS & EXCEPTION INTELLIGENCE")
    print("=" * 70)

    milestone_results = [
        {
            "deal_id": "DEAL-001",
            "execution_state": "ACQUISITION_ACTIVE",
            "execution_status": "MILESTONE_ADVANCED",
            "current_milestone": "SELLER_CONTACT",
            "completed_count": 1,
            "milestone_count": 6,
            "milestones": [
                {
                    "milestone": "EXECUTION_INITIATED",
                    "sequence": 1,
                    "status": "COMPLETED",
                },
                {
                    "milestone": "SELLER_CONTACT",
                    "sequence": 2,
                    "status": "CURRENT",
                },
                {
                    "milestone": "PROPERTY_DUE_DILIGENCE",
                    "sequence": 3,
                    "status": "PENDING",
                },
                {
                    "milestone": "NEGOTIATION",
                    "sequence": 4,
                    "status": "PENDING",
                },
                {
                    "milestone": "PURCHASE_AGREEMENT",
                    "sequence": 5,
                    "status": "PENDING",
                },
                {
                    "milestone": "ACQUISITION_COMPLETED",
                    "sequence": 6,
                    "status": "PENDING",
                },
            ],
        },
        {
            "deal_id": "DEAL-002",
            "execution_state": "ACQUISITION_BLOCKED",
            "execution_status": "EXECUTION_BLOCKED",
            "current_milestone": None,
            "completed_count": 0,
            "milestone_count": 6,
            "milestones": [],
        },
        {
            "deal_id": "DEAL-003",
            "execution_state": "ACQUISITION_ACTIVE",
            "execution_status": "ACQUISITION_EXECUTION_ACTIVE",
            "current_milestone": "PROPERTY_DUE_DILIGENCE",
            "completed_count": 2,
            "milestone_count": 6,
            "milestones": [
                {
                    "milestone": "EXECUTION_INITIATED",
                    "sequence": 1,
                    "status": "COMPLETED",
                },
                {
                    "milestone": "SELLER_CONTACT",
                    "sequence": 2,
                    "status": "COMPLETED",
                },
                {
                    "milestone": "PROPERTY_DUE_DILIGENCE",
                    "sequence": 3,
                    "status": "CURRENT",
                },
                {
                    "milestone": "NEGOTIATION",
                    "sequence": 4,
                    "status": "PENDING",
                },
                {
                    "milestone": "PURCHASE_AGREEMENT",
                    "sequence": 5,
                    "status": "PENDING",
                },
                {
                    "milestone": "ACQUISITION_COMPLETED",
                    "sequence": 6,
                    "status": "PENDING",
                },
            ],
        },
    ]

    print("\nSTEP 1 - Loading Acquisition Milestone Execution Results")
    pprint(milestone_results)

    integration = AcquisitionProgressIntegration()

    print("\nSTEP 2 - Running Acquisition Progress Intelligence")
    result = integration.evaluate(milestone_results)
    pprint(result)

    print("\nSTEP 3 - Normal Progress")
    pprint(result["normal_progress"])

    print("\nSTEP 4 - Blocked Acquisitions")
    pprint(result["blocked"])

    print("\nSTEP 5 - Human Review Required")
    pprint(result["review_required"])

    print("\nSTEP 6 - Ready To Advance")
    pprint(result["ready_to_advance"])

    print("\nSTEP 7 - Validation")

    assert result["status"] == (
        "ACQUISITION_PROGRESS_INTEGRATION_COMPLETE"
    )

    assert result["progress"]["status"] == (
        "ACQUISITION_PROGRESS_ANALYZED"
    )

    assert len(result["progress"]["analyses"]) == 3

    assert len(result["normal_progress"]) == 2

    assert len(result["blocked"]) == 1

    assert result["blocked"][0]["deal_id"] == "DEAL-002"

    assert result["blocked"][0]["progress_status"] == "BLOCKED"

    assert len(result["review_required"]) == 0

    assert len(result["ready_to_advance"]) == 0

    deal_001 = next(
        item
        for item in result["progress"]["analyses"]
        if item["deal_id"] == "DEAL-001"
    )

    assert deal_001["progress_status"] == "NORMAL_PROGRESS"

    deal_002 = next(
        item
        for item in result["progress"]["analyses"]
        if item["deal_id"] == "DEAL-002"
    )

    assert deal_002["progress_status"] == "BLOCKED"

    deal_003 = next(
        item
        for item in result["progress"]["analyses"]
        if item["deal_id"] == "DEAL-003"
    )

    assert deal_003["progress_status"] == "NORMAL_PROGRESS"

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 25 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
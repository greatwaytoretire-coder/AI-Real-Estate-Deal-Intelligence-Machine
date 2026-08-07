from __future__ import annotations

from pprint import pprint

from ai_real_estate_deal_intelligence_machine.learning.acquisition_exception_resolution_integration import (
    AcquisitionExceptionResolutionIntegration,
)


def build_progress_result():
    return {
        "progress": {
            "analyses": [
                {
                    "deal_id": "DEAL-001",
                    "completed_count": 1,
                    "current_milestone": "SELLER_CONTACT",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "execution_status": "MILESTONE_ADVANCED",
                    "milestone_count": 6,
                    "progress_status": "NORMAL_PROGRESS",
                    "exception_type": None,
                    "recommendation": (
                        "Acquisition is progressing normally "
                        "through its milestone plan."
                    ),
                    "status": "ACQUISITION_PROGRESS_CLASSIFIED",
                },
                {
                    "deal_id": "DEAL-002",
                    "completed_count": 0,
                    "current_milestone": None,
                    "execution_state": "ACQUISITION_BLOCKED",
                    "execution_status": "EXECUTION_BLOCKED",
                    "milestone_count": 6,
                    "progress_status": "BLOCKED",
                    "exception_type": "ACQUISITION_BLOCKED",
                    "recommendation": (
                        "Do not advance the acquisition until "
                        "the blocking condition is resolved."
                    ),
                    "status": "ACQUISITION_PROGRESS_CLASSIFIED",
                },
                {
                    "deal_id": "DEAL-003",
                    "completed_count": 2,
                    "current_milestone": "PROPERTY_DUE_DILIGENCE",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "execution_status": "ACQUISITION_EXECUTION_ACTIVE",
                    "milestone_count": 6,
                    "progress_status": "READY_TO_ADVANCE",
                    "exception_type": None,
                    "recommendation": (
                        "The acquisition is ready to advance "
                        "to the next milestone."
                    ),
                    "status": "ACQUISITION_PROGRESS_CLASSIFIED",
                },
                {
                    "deal_id": "DEAL-004",
                    "completed_count": 2,
                    "current_milestone": "NEGOTIATION",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "execution_status": "ACQUISITION_EXECUTION_ACTIVE",
                    "milestone_count": 6,
                    "progress_status": "STALLED",
                    "exception_type": "MILESTONE_STALLED",
                    "recommendation": (
                        "Investigate the stalled acquisition "
                        "milestone."
                    ),
                    "status": "ACQUISITION_PROGRESS_CLASSIFIED",
                },
                {
                    "deal_id": "DEAL-005",
                    "completed_count": 3,
                    "current_milestone": "PURCHASE_AGREEMENT",
                    "execution_state": "ACQUISITION_ACTIVE",
                    "execution_status": "ACQUISITION_EXECUTION_ACTIVE",
                    "milestone_count": 6,
                    "progress_status": "REVIEW_REQUIRED",
                    "exception_type": "MANUAL_REVIEW_REQUIRED",
                    "recommendation": (
                        "Human review is required before "
                        "additional execution."
                    ),
                    "status": "ACQUISITION_PROGRESS_CLASSIFIED",
                },
            ],
            "status": "ACQUISITION_PROGRESS_ANALYZED",
            "summary": {
                "blocked_count": 1,
                "normal_count": 1,
                "ready_to_advance_count": 1,
                "review_count": 1,
                "stalled_count": 1,
                "total_acquisitions": 5,
            },
        },
        "status": "ACQUISITION_PROGRESS_INTEGRATION_COMPLETE",
    }


def main():
    print("=" * 70)
    print("SPRINT 4 PART 26 INTEGRATION TEST")
    print("ACQUISITION EXCEPTION RESOLUTION INTELLIGENCE")
    print("=" * 70)

    progress_result = build_progress_result()

    print("\nSTEP 1 - Loading Acquisition Progress Results")
    pprint(progress_result)

    integration = AcquisitionExceptionResolutionIntegration()

    print("\nSTEP 2 - Running Exception Resolution Intelligence")

    result = integration.evaluate(progress_result)

    pprint(result)

    print("\nSTEP 3 - Resolution Results")

    for resolution in result["resolution"]["resolutions"]:
        print(
            f"{resolution['deal_id']} | "
            f"Progress: {resolution['progress_status']} | "
            f"Resolution: {resolution['resolution_type']} | "
            f"Action: {resolution['resolution_action']} | "
            f"Status: {resolution['resolution_status']}"
        )

    print("\nSTEP 4 - Action Required")
    pprint(result["action_required"])

    print("\nSTEP 5 - Human Review Required")
    pprint(result["human_review_required"])

    print("\nSTEP 6 - Ready To Advance")
    pprint(result["ready_to_advance"])

    print("\nSTEP 7 - Normal Continuation")
    pprint(result["normal_continuation"])

    print("\nSTEP 8 - Resolution Summary")
    pprint(result["resolution"]["summary"])

    print("\nSTEP 9 - Validation")

    assert result["status"] == (
        "ACQUISITION_EXCEPTION_RESOLUTION_INTEGRATION_COMPLETE"
    )

    resolutions = result["resolution"]["resolutions"]

    assert len(resolutions) == 5

    assert result["resolution"]["summary"][
        "blocked_resolution_count"
    ] == 1

    assert result["resolution"]["summary"][
        "stalled_resolution_count"
    ] == 1

    assert result["resolution"]["summary"][
        "human_review_count"
    ] == 3

    assert result["resolution"]["summary"][
        "ready_to_advance_count"
    ] == 1

    assert result["resolution"]["summary"][
        "normal_continuation_count"
    ] == 1

    blocked = next(
        item
        for item in resolutions
        if item["deal_id"] == "DEAL-002"
    )

    assert blocked["resolution_action"] == (
        "RESOLVE_BLOCKING_CONDITION"
    )

    stalled = next(
        item
        for item in resolutions
        if item["deal_id"] == "DEAL-004"
    )

    assert stalled["resolution_action"] == (
        "RECOVER_STALLED_ACQUISITION"
    )

    ready = next(
        item
        for item in resolutions
        if item["deal_id"] == "DEAL-003"
    )

    assert ready["resolution_action"] == (
        "ADVANCE_ACQUISITION_MILESTONE"
    )

    review = next(
        item
        for item in resolutions
        if item["deal_id"] == "DEAL-005"
    )

    assert review["resolution_action"] == (
        "ROUTE_TO_HUMAN_REVIEW"
    )

    normal = next(
        item
        for item in resolutions
        if item["deal_id"] == "DEAL-001"
    )

    assert normal["resolution_action"] == (
        "CONTINUE_CURRENT_MILESTONE"
    )

    print("Validation successful")

    print("\n" + "=" * 70)
    print("SPRINT 4 PART 26 INTEGRATION TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
from ai_real_estate_deal_intelligence_machine.acquisition.due_diligence.due_diligence_engine import (
    DueDiligenceEngine,
    DueDiligenceStatus,
)


def test_create_due_diligence_case():

    engine = DueDiligenceEngine()

    case = engine.create_review(
        review_id="DD-001",
        property_address="123 Main Street",
        contract_id="CONTRACT-001",
    )

    assert case.review_id == "DD-001"
    assert case.property_address == "123 Main Street"
    assert case.contract_id == "CONTRACT-001"
    assert case.status == DueDiligenceStatus.INITIATED



def test_get_reviews():

    engine = DueDiligenceEngine()

    engine.create_review(
        review_id="DD-002",
        property_address="456 Oak Avenue",
        contract_id="CONTRACT-002",
    )

    reviews = engine.get_reviews()

    assert len(reviews) == 1
    assert reviews[0].review_id == "DD-002"



def test_update_due_diligence_status():

    engine = DueDiligenceEngine()

    engine.create_review(
        review_id="DD-003",
        property_address="789 Pine Road",
        contract_id="CONTRACT-003",
    )

    updated = engine.update_status(
        review_id="DD-003",
        new_status=DueDiligenceStatus.IN_PROGRESS,
        note="Inspection review started.",
    )

    assert updated.status == DueDiligenceStatus.IN_PROGRESS
    assert "Inspection review started." in updated.notes



def test_complete_due_diligence():

    engine = DueDiligenceEngine()

    review = engine.create_review(
        review_id="DD-004",
        property_address="321 Elm Street",
        contract_id="CONTRACT-004",
    )

    engine.update_status(
        review_id=review.review_id,
        new_status=DueDiligenceStatus.COMPLETED,
        note="All documents verified.",
    )

    assert review.status == DueDiligenceStatus.COMPLETED



def test_missing_due_diligence_review():

    engine = DueDiligenceEngine()

    try:

        engine.update_status(
            review_id="INVALID",
            new_status=DueDiligenceStatus.COMPLETED,
            note="Missing review.",
        )

        assert False

    except ValueError as error:

        assert str(error) == "Due diligence review not found."
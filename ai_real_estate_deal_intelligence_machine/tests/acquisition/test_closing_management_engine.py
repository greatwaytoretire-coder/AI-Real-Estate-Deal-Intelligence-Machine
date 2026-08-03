from ai_real_estate_deal_intelligence_machine.acquisition.closing.closing_management_engine import (
    ClosingManagementEngine,
    ClosingStatus,
)



def test_create_closing():

    engine = ClosingManagementEngine()


    closing = engine.create_closing(
        closing_id="CLOSING-001",
        contract_id="CONTRACT-001",
        property_address="123 Main Street",
        title_company="ABC Title",
        closing_date="2026-08-15",
    )


    assert closing.closing_id == "CLOSING-001"
    assert closing.status == ClosingStatus.SCHEDULED



def test_get_closings():

    engine = ClosingManagementEngine()


    engine.create_closing(
        closing_id="CLOSING-002",
        contract_id="CONTRACT-002",
        property_address="456 Oak Avenue",
        title_company="XYZ Title",
        closing_date="2026-08-20",
    )


    closings = engine.get_closings()


    assert len(closings) == 1
    assert closings[0].closing_id == "CLOSING-002"



def test_update_closing_status():

    engine = ClosingManagementEngine()


    engine.create_closing(
        closing_id="CLOSING-003",
        contract_id="CONTRACT-003",
        property_address="789 Pine Road",
        title_company="ABC Title",
        closing_date="2026-08-25",
    )


    updated = engine.update_status(
        closing_id="CLOSING-003",
        new_status=ClosingStatus.FUNDED,
        note="Funding completed.",
    )


    assert updated.status == ClosingStatus.FUNDED
    assert "Funding completed." in updated.notes



def test_add_document():

    engine = ClosingManagementEngine()


    closing = engine.create_closing(
        closing_id="CLOSING-004",
        contract_id="CONTRACT-004",
        property_address="321 Elm Street",
        title_company="XYZ Title",
        closing_date="2026-08-30",
    )


    engine.add_document(
        closing_id=closing.closing_id,
        document_name="Purchase Agreement",
    )


    assert "Purchase Agreement" in closing.documents



def test_missing_closing():

    engine = ClosingManagementEngine()


    try:

        engine.update_status(
            closing_id="INVALID",
            new_status=ClosingStatus.COMPLETED,
            note="Missing closing.",
        )

        assert False


    except ValueError as error:

        assert str(error) == "Closing not found."
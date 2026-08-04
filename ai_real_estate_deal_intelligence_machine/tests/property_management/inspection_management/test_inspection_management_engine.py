from ai_real_estate_deal_intelligence_machine.property_management.inspection_management.inspection_management_engine import (
    InspectionManagementEngine,
)



def test_create_inspection():

    engine = InspectionManagementEngine()


    inspection = engine.create_inspection(
        inspection_id="INS-001",
        property_id="PROP-001",
        inspector_name="John Inspector",
        inspection_date="2026-01-01",
        condition="GOOD",
    )


    assert inspection.inspection_id == "INS-001"

    assert inspection.status == "COMPLETED"



def test_get_inspections():

    engine = InspectionManagementEngine()


    engine.create_inspection(
        inspection_id="INS-002",
        property_id="PROP-002",
        inspector_name="Jane Inspector",
        inspection_date="2026-01-01",
        condition="FAIR",
    )


    inspections = engine.get_inspections()


    assert len(inspections) == 1



def test_update_status():

    engine = InspectionManagementEngine()


    engine.create_inspection(
        inspection_id="INS-003",
        property_id="PROP-003",
        inspector_name="Inspector",
        inspection_date="2026-01-01",
        condition="POOR",
    )


    inspection = engine.update_status(
        "INS-003",
        "FOLLOW_UP_REQUIRED",
    )


    assert inspection.status == "FOLLOW_UP_REQUIRED"



def test_missing_inspection():

    engine = InspectionManagementEngine()


    try:

        engine.get_inspection(
            "BAD"
        )


        assert False


    except ValueError:

        assert True
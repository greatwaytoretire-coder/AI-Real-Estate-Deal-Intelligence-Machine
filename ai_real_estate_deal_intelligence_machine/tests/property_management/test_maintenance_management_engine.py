from ai_real_estate_deal_intelligence_machine.property_management.maintenance_management_engine import (
    MaintenanceManagementEngine,
    PriorityLevel,
    WorkOrderStatus,
)


def test_create_work_order():

    engine = MaintenanceManagementEngine()

    order = engine.create_work_order(
        work_order_id="WO-001",
        property_id="PROP-001",
        description="Repair HVAC",
        priority=PriorityLevel.HIGH,
        estimated_cost=500,
    )

    assert order.work_order_id == "WO-001"
    assert order.status == WorkOrderStatus.OPEN



def test_assign_vendor():

    engine = MaintenanceManagementEngine()

    engine.create_work_order(
        "WO-002",
        "PROP-002",
        "Roof repair",
        PriorityLevel.MEDIUM,
        1000,
    )

    order = engine.assign_vendor(
        "WO-002",
        "ABC Roofing",
    )

    assert order.vendor == "ABC Roofing"
    assert order.status == WorkOrderStatus.ASSIGNED



def test_complete_work_order():

    engine = MaintenanceManagementEngine()

    engine.create_work_order(
        "WO-003",
        "PROP-003",
        "Plumbing repair",
        PriorityLevel.LOW,
        200,
    )

    order = engine.complete_work_order(
        "WO-003"
    )

    assert order.status == WorkOrderStatus.COMPLETED



def test_missing_work_order():

    engine = MaintenanceManagementEngine()

    try:
        engine.get_work_order("BAD")

        assert False

    except ValueError:

        assert True
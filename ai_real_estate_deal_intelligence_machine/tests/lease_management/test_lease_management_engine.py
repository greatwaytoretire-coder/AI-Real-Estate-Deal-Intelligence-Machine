from ai_real_estate_deal_intelligence_machine.lease_management.lease_management_engine import (
    LeaseManagementEngine,
)


def test_create_lease():

    engine = LeaseManagementEngine()

    lease = engine.create_lease(
        lease_id="LEASE-001",
        tenant_id="TENANT-001",
        property_id="PROPERTY-001",
        start_date="2026-01-01",
        end_date="2027-01-01",
        monthly_rent=1500,
    )

    assert lease.lease_id == "LEASE-001"
    assert lease.status == "ACTIVE"



def test_get_leases():

    engine = LeaseManagementEngine()

    engine.create_lease(
        lease_id="LEASE-002",
        tenant_id="TENANT-002",
        property_id="PROPERTY-002",
        start_date="2026-01-01",
        end_date="2027-01-01",
        monthly_rent=1800,
    )

    leases = engine.get_leases()

    assert len(leases) == 1



def test_update_status():

    engine = LeaseManagementEngine()

    engine.create_lease(
        lease_id="LEASE-003",
        tenant_id="TENANT-003",
        property_id="PROPERTY-003",
        start_date="2026-01-01",
        end_date="2027-01-01",
        monthly_rent=1200,
    )

    lease = engine.update_status(
        "LEASE-003",
        "EXPIRED"
    )

    assert lease.status == "EXPIRED"



def test_missing_lease():

    engine = LeaseManagementEngine()

    try:
        engine.get_lease("BAD")

        assert False

    except ValueError:
        assert True
from ai_real_estate_deal_intelligence_machine.property_management.tenant_management_engine import (
    TenantManagementEngine,
    TenantStatus,
)


def test_create_tenant():

    engine = TenantManagementEngine()

    tenant = engine.create_tenant(
        tenant_id="TEN-001",
        property_id="PROP-001",
        name="John Smith",
        lease_start="2026-01-01",
        lease_end="2027-01-01",
        monthly_rent=1500,
    )

    assert tenant.tenant_id == "TEN-001"
    assert tenant.status == TenantStatus.ACTIVE



def test_get_tenants():

    engine = TenantManagementEngine()

    engine.create_tenant(
        tenant_id="TEN-002",
        property_id="PROP-002",
        name="Jane Doe",
        lease_start="2026-01-01",
        lease_end="2027-01-01",
        monthly_rent=1800,
    )

    tenants = engine.get_tenants()

    assert len(tenants) == 1



def test_update_status():

    engine = TenantManagementEngine()

    engine.create_tenant(
        tenant_id="TEN-003",
        property_id="PROP-003",
        name="Tenant",
        lease_start="2026-01-01",
        lease_end="2027-01-01",
        monthly_rent=1200,
    )

    tenant = engine.update_status(
        "TEN-003",
        TenantStatus.DELINQUENT,
    )

    assert tenant.status == TenantStatus.DELINQUENT



def test_missing_tenant():

    engine = TenantManagementEngine()

    try:
        engine.get_tenant("BAD")

        assert False

    except ValueError:
        assert True
from dataclasses import dataclass
from enum import Enum


class TenantStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELINQUENT = "DELINQUENT"


@dataclass
class Tenant:
    tenant_id: str
    property_id: str
    tenant_name: str
    monthly_rent: float
    lease_start: str | None = None
    lease_end: str | None = None
    status: TenantStatus = TenantStatus.ACTIVE


class TenantManagementEngine:
    """
    Tenant lifecycle management engine.

    Supports:
    - API tenant_name interface
    - Legacy name + lease dates interface
    """

    def __init__(self):
        self.tenants = {}


    def create_tenant(
        self,
        tenant_id: str,
        property_id: str,
        monthly_rent: float,
        tenant_name: str | None = None,
        name: str | None = None,
        lease_start: str | None = None,
        lease_end: str | None = None,
    ):

        resolved_name = tenant_name or name

        if resolved_name is None:
            raise ValueError(
                "Tenant name is required."
            )

        tenant = Tenant(
            tenant_id=tenant_id,
            property_id=property_id,
            tenant_name=resolved_name,
            monthly_rent=monthly_rent,
            lease_start=lease_start,
            lease_end=lease_end,
        )

        self.tenants[tenant_id] = tenant

        return tenant


    def get_tenants(self):

        return list(self.tenants.values())


    def get_tenant(self, tenant_id: str):

        tenant = self.tenants.get(tenant_id)

        if tenant is None:
            raise ValueError(
                "Tenant not found."
            )

        return tenant


    def update_status(
        self,
        tenant_id: str,
        status: TenantStatus,
    ):

        tenant = self.get_tenant(
            tenant_id
        )

        tenant.status = status

        return tenant


    def remove_tenant(
        self,
        tenant_id: str,
    ):

        tenant = self.get_tenant(
            tenant_id
        )

        del self.tenants[tenant_id]

        return tenant
from dataclasses import dataclass
from typing import List


@dataclass
class Lease:
    lease_id: str
    tenant_id: str
    property_id: str
    start_date: str
    end_date: str
    monthly_rent: float
    status: str = "ACTIVE"


class LeaseManagementEngine:

    def __init__(self):
        self.leases: List[Lease] = []


    def create_lease(
        self,
        lease_id: str,
        tenant_id: str,
        property_id: str,
        start_date: str,
        end_date: str,
        monthly_rent: float,
    ):

        if monthly_rent <= 0:
            raise ValueError(
                "Monthly rent must be greater than zero."
            )

        lease = Lease(
            lease_id=lease_id,
            tenant_id=tenant_id,
            property_id=property_id,
            start_date=start_date,
            end_date=end_date,
            monthly_rent=monthly_rent,
        )

        self.leases.append(lease)

        return lease


    def get_lease(self, lease_id: str):

        for lease in self.leases:
            if lease.lease_id == lease_id:
                return lease

        raise ValueError(
            "Lease not found."
        )


    def get_leases(self):

        return self.leases


    def update_status(
        self,
        lease_id: str,
        status: str
    ):

        lease = self.get_lease(lease_id)

        lease.status = status

        return lease
from pydantic import BaseModel


class LeaseCreateRequest(BaseModel):

    lease_id: str
    tenant_id: str
    property_id: str
    start_date: str
    end_date: str
    monthly_rent: float
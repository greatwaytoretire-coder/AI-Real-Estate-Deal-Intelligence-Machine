from pydantic import BaseModel, Field


class TenantCreateRequest(BaseModel):
    tenant_id: str = Field(..., min_length=1)
    property_id: str = Field(..., min_length=1)
    tenant_name: str = Field(..., min_length=1)
    monthly_rent: float = Field(..., gt=0)


class TenantResponse(BaseModel):
    tenant_id: str
    property_id: str
    tenant_name: str
    monthly_rent: float
    status: str


class TenantStatusUpdateRequest(BaseModel):
    status: str = Field(..., min_length=1)
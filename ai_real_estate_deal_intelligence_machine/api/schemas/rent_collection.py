from pydantic import BaseModel


class RentPaymentCreateRequest(BaseModel):

    payment_id: str
    tenant_id: str
    property_id: str
    amount: float
    payment_date: str
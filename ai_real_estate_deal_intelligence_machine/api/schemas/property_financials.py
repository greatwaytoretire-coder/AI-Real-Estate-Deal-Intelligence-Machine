from pydantic import BaseModel


class PropertyFinancialCreateRequest(BaseModel):

    record_id: str
    property_id: str
    income: float
    expenses: float
    period: str
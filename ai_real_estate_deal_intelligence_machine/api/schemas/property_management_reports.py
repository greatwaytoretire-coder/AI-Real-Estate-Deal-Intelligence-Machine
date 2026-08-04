from pydantic import BaseModel


class PropertyManagementReportCreateRequest(BaseModel):

    report_id: str
    property_id: str
    income: float
    expenses: float
    period: str
from pydantic import BaseModel


class MaintenanceRequest(BaseModel):

    work_order_id: str
    property_id: str
    description: str
    priority: str
    estimated_cost: float
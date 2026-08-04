from pydantic import BaseModel



class InspectionCreateRequest(BaseModel):

    inspection_id: str
    property_id: str
    inspector_name: str
    inspection_date: str
    condition: str
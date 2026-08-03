from pydantic import BaseModel



class AcquisitionDealResponse(BaseModel):

    deal_id: str

    seller_id: str

    property_address: str

    estimated_value: float

    repair_cost: float

    recommended_offer: float

    status: str

    notes: list[str]



class AcquisitionDealStatusRequest(BaseModel):

    deal_id: str

    new_status: str

    note: str
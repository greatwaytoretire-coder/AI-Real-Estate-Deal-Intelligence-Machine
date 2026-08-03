from pydantic import BaseModel


class AcquisitionWorkflowRequest(BaseModel):

    seller_id: str

    new_stage: str

    note: str



class AcquisitionWorkflowResponse(BaseModel):

    seller_id: str

    property_address: str

    current_stage: str

    offer_amount: float

    notes: list[str]
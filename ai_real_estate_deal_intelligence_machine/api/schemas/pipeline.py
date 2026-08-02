from pydantic import BaseModel


class AcquisitionPipelineRequest(BaseModel):

    property_id: str

    purchase_price: float

    estimated_value: float

    repair_cost: float



class AcquisitionPipelineResponse(BaseModel):

    property_id: str

    qualified: bool

    deal_score: float

    recommendation: str

    status: str
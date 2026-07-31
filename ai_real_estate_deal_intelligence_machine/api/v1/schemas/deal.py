from pydantic import BaseModel


class DealAnalysisRequest(BaseModel):

    property_id: str
    address: str
    purchase_price: float


class DealAnalysisResponse(BaseModel):

    property_id: str
    analysis_status: str 
from pydantic import BaseModel, ConfigDict


class DueDiligenceCreate(BaseModel):

    review_id: str
    property_address: str
    contract_id: str



class DueDiligenceResponse(BaseModel):

    review_id: str
    property_address: str
    contract_id: str
    status: str
    notes: list[str]

    model_config = ConfigDict(
        from_attributes=True
    )
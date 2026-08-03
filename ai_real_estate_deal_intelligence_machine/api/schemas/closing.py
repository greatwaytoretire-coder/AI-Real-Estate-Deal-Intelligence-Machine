from pydantic import BaseModel, ConfigDict



class ClosingCreate(BaseModel):

    closing_id: str
    contract_id: str
    property_address: str
    title_company: str
    closing_date: str



class ClosingResponse(BaseModel):

    closing_id: str
    contract_id: str
    property_address: str
    title_company: str
    closing_date: str
    status: str
    documents: list[str]
    notes: list[str]


    model_config = ConfigDict(
        from_attributes=True
    )
from pydantic import BaseModel, ConfigDict



class ContractCreate(BaseModel):

    contract_id: str

    seller_id: str

    property_address: str

    purchase_price: float

    earnest_money: float



class ContractResponse(BaseModel):

    contract_id: str

    seller_id: str

    property_address: str

    purchase_price: float

    earnest_money: float

    status: str

    notes: list[str]


    model_config = ConfigDict(
        from_attributes=True
    )
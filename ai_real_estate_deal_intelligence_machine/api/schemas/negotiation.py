from pydantic import BaseModel


class NegotiationAnalysisRequest(BaseModel):
    deal_id: str

    current_offer: float

    seller_counter_offer: float

    arv: float


class NegotiationAnalysisResponse(BaseModel):
    deal_id: str

    current_offer: float

    seller_counter_offer: float

    arv: float

    negotiation_stage: str

    recommended_offer: float

    acceptance_probability: float

    reasoning: list[str]
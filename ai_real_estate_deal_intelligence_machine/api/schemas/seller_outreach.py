from pydantic import BaseModel


class SellerOutreachRequest(BaseModel):

    seller_id: str

    property_id: str

    motivation_level: str

    preferred_channel: str = "phone"



class SellerOutreachResponse(BaseModel):

    seller_id: str

    property_id: str

    outreach_channel: str

    priority: str

    message: str

    status: str
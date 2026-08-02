from pydantic import BaseModel


class BuyerOutreachRequest(BaseModel):

    property_id: str

    buyer_id: str

    buyer_type: str

    preferred_channel: str = "email"



class BuyerOutreachResponse(BaseModel):

    property_id: str

    buyer_id: str

    outreach_channel: str

    priority: str

    message: str

    status: str
from dataclasses import dataclass


@dataclass
class SellerOutreachPackage:

    seller_id: str

    property_id: str

    outreach_channel: str

    priority: str

    message: str

    status: str



class SellerOutreachEngine:
    """
    Generates acquisition outreach
    recommendations for motivated sellers.
    """


    def generate(
        self,
        seller_id: str,
        property_id: str,
        motivation_level: str,
        preferred_channel: str = "phone",
    ) -> SellerOutreachPackage:


        priority = "MEDIUM"


        if motivation_level.lower() in [
            "high",
            "urgent",
            "distressed",
        ]:

            priority = "HIGH"



        message = (
            f"Hello, we are reaching out regarding "
            f"your property {property_id}. "
            f"We specialize in helping property owners "
            f"explore flexible selling options."
        )


        return SellerOutreachPackage(

            seller_id=seller_id,

            property_id=property_id,

            outreach_channel=preferred_channel,

            priority=priority,

            message=message,

            status="READY",

        )
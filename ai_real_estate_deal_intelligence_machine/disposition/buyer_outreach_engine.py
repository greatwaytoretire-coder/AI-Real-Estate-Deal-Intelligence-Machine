from dataclasses import dataclass


@dataclass
class BuyerOutreachPackage:
    property_id: str
    buyer_id: str
    outreach_channel: str
    priority: str
    message: str
    status: str


class BuyerOutreachEngine:
    """
    Creates disposition outreach recommendations
    for matched real estate buyers.
    """

    def generate(
        self,
        property_id: str,
        buyer_id: str,
        buyer_type: str,
        preferred_channel: str = "email",
    ) -> BuyerOutreachPackage:

        priority = "HIGH"

        if buyer_type.lower() == "wholesaler":
            priority = "MEDIUM"

        message = (
            f"New investment opportunity available for "
            f"property {property_id}. "
            f"Based on your buying profile, this deal "
            f"may match your acquisition criteria."
        )

        return BuyerOutreachPackage(
            property_id=property_id,
            buyer_id=buyer_id,
            outreach_channel=preferred_channel,
            priority=priority,
            message=message,
            status="READY",
        )
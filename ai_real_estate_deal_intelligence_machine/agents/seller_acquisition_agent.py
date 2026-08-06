from ai_real_estate_deal_intelligence_machine.acquisition.seller_lead_pipeline import (
    SellerLeadPipeline,
)


class SellerAcquisitionAgent:
    """
    Converts seller opportunities into acquisition decisions.
    """

    def __init__(self):
        self.pipeline = SellerLeadPipeline()


    def process(self, payload):

        results = self.pipeline.analyze_lead(
            market=payload["market"],
            property_address=payload["property_address"],
            estimated_value=payload["estimated_value"],
            motivation_score=payload["motivation_score"],
            distress_signals=payload["distress_signals"],
        )

        result = results[0]

        return {
            "agent": "seller_acquisition",
            "decision": result.recommendation,
            "priority_score": result.priority_score,
            "reasoning": result.reasoning,
        }
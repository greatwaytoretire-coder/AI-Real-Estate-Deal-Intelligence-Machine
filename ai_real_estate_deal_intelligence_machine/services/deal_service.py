from ai_real_estate_deal_intelligence_machine.repositories.deal_repository import (
    DealRepository,
)


class DealService:

    def __init__(
        self,
        repository: DealRepository,
    ):
        self.repository = repository


    def create_deal(
        self,
        deal_data: dict,
    ):

        return self.repository.create_deal(
            deal_data
        )


    def analyze_deal(
        self,
        deal_data: dict,
    ):

        saved_deal = self.repository.create_deal(
            deal_data
        )

        return {
            "deal": saved_deal,
            "analysis_status": "completed",
        }


    def get_deal(
        self,
        property_id: str,
    ):

        return self.repository.get_deal(
            property_id
        )


    def list_deals(self):

        return self.repository.list_deals()
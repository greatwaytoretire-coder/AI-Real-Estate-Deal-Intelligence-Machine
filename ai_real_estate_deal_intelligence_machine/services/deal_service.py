from ai_real_estate_deal_intelligence_machine.repositories.deal_repository import (
    DealRepository,
)


class DealService:

    def __init__(
        self,
        repository: DealRepository,
    ):
        self.repository = repository


    def analyze_deal(
        self,
        deal,
    ):

        saved_deal = self.repository.save_deal(
            deal
        )

        return {
            "deal": saved_deal,
            "analysis_status": "completed",
        }


    def get_deal(
        self,
        deal_id: str,
    ):

        return self.repository.get_deal(
            deal_id
        )
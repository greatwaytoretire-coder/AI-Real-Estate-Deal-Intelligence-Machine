from typing import Dict, List, Optional

from ai_real_estate_deal_intelligence_machine.database.models import (
    DealRecord,
)



class DealRepository:
    """
    Deal persistence abstraction.

    Sprint 4 starts with memory storage.

    Future:
    SQLite
    PostgreSQL
    Cloud database
    """


    def __init__(self):

        self._deals: Dict[str, DealRecord] = {}



    def save_deal(
        self,
        deal: DealRecord,
    ) -> DealRecord:

        self._deals[
            deal.deal_id
        ] = deal

        return deal



    def get_deal(
        self,
        deal_id: str,
    ) -> Optional[DealRecord]:

        return self._deals.get(
            deal_id
        )



    def list_deals(
        self,
    ) -> List[DealRecord]:

        return list(
            self._deals.values()
        )



    def update_status(
        self,
        deal_id: str,
        status: str,
    ):

        deal = self.get_deal(
            deal_id
        )

        if deal:

            deal.status = status

        return deal
from sqlalchemy.orm import Session


class DealRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_deal(self, deal_id: str):

        return {
            "property_id": deal_id,
            "address": "123 Example Street",
            "status": "discovered",
        }


    def save_deal(self, deal):

        return {
            "saved": True,
            "deal": deal,
        }
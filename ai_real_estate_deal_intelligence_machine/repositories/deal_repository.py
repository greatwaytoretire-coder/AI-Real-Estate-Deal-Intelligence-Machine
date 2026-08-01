from sqlalchemy.orm import Session

from ai_real_estate_deal_intelligence_machine.models.deal import DealModel


class DealRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_deal(self, deal_id: str):

        return (
            self.db.query(DealModel)
            .filter(
                DealModel.property_id == deal_id
            )
            .first()
        )


    def create_deal(self, deal_data: dict):

        existing = (
            self.db.query(DealModel)
            .filter(
                DealModel.property_id == deal_data["property_id"]
            )
            .first()
        )

        if existing:

            for key, value in deal_data.items():
                setattr(
                    existing,
                    key,
                    value
                )

            self.db.commit()
            self.db.refresh(existing)

            return existing


        deal = DealModel(
            **deal_data
        )

        self.db.add(deal)

        self.db.commit()

        self.db.refresh(deal)

        return deal


    def save_deal(self, deal):

        return self.create_deal(deal)
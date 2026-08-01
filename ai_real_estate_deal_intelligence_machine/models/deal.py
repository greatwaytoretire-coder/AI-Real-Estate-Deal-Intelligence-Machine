from sqlalchemy import Column, Integer, String
from ai_real_estate_deal_intelligence_machine.database.base import Base


class DealModel(Base):

    __tablename__ = "deals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    address = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        default="new",
    )
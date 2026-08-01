from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
)

from ai_real_estate_deal_intelligence_machine.database.base import Base


class DealModel(Base):

    __tablename__ = "deals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    property_id = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    address = Column(
        String,
        nullable=False,
    )

    city = Column(
        String,
        nullable=True,
    )

    state = Column(
        String,
        nullable=True,
    )

    zip_code = Column(
        String,
        nullable=True,
    )

    purchase_price = Column(
        Float,
        nullable=True,
    )

    estimated_value = Column(
        Float,
        nullable=True,
    )

    repair_cost = Column(
        Float,
        nullable=True,
    )

    projected_profit = Column(
        Float,
        nullable=True,
    )

    deal_score = Column(
        Float,
        nullable=True,
    )

    status = Column(
        String,
        default="new",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
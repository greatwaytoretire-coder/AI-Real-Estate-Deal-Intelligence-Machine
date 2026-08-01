from sqlalchemy import Column, Integer, String

from ai_real_estate_deal_intelligence_machine.database.base import Base


class UserModel(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password = Column(
        String,
        nullable=False,
    )

    role = Column(
        String,
        default="investor",
        nullable=False,
    )
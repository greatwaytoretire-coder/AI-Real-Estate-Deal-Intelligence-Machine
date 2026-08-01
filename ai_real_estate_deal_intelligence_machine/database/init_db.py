from ai_real_estate_deal_intelligence_machine.database.base import Base
from ai_real_estate_deal_intelligence_machine.database.session import engine
from ai_real_estate_deal_intelligence_machine import models


def init_database():

    Base.metadata.create_all(
        bind=engine
    )


if __name__ == "__main__":
    init_database()
from sqlalchemy.orm import Session

from ai_real_estate_deal_intelligence_machine.database.session import get_db

from ai_real_estate_deal_intelligence_machine.repositories.deal_repository import (
    DealRepository,
)

from ai_real_estate_deal_intelligence_machine.services.deal_service import (
    DealService,
)


def get_database() -> Session:
    return next(get_db())


def get_deal_service() -> DealService:
    db = next(get_db())

    repository = DealRepository(db)

    return DealService(repository)
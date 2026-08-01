from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ai_real_estate_deal_intelligence_machine.database.base import Base
from ai_real_estate_deal_intelligence_machine.repositories.user_repository import (
    UserRepository,
)
from ai_real_estate_deal_intelligence_machine.services.user_service import (
    UserService,
)


def test_user_registration_and_authentication():

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={
            "check_same_thread": False
        },
    )

    TestingSessionLocal = sessionmaker(
        bind=engine
    )

    Base.metadata.create_all(
        bind=engine
    )

    db = TestingSessionLocal()

    repository = UserRepository(db)

    service = UserService(repository)

    user = service.register_user(
        email="test@example.com",
        password="SecurePassword123!",
        role="investor",
    )

    assert user.email == "test@example.com"

    authenticated = service.authenticate_user(
        email="test@example.com",
        password="SecurePassword123!",
    )

    assert authenticated.email == "test@example.com"

    db.close()
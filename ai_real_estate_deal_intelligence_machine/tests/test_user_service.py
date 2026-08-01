from ai_real_estate_deal_intelligence_machine.repositories.user_repository import (
    UserRepository,
)

from ai_real_estate_deal_intelligence_machine.services.user_service import (
    UserService,
)


def test_user_registration_and_authentication():

    repository = UserRepository()

    service = UserService(repository)


    user = service.register_user(
        "investor@test.com",
        "SecurePassword123!",
    )


    assert user["email"] == "investor@test.com"


    authenticated = service.authenticate_user(
        "investor@test.com",
        "SecurePassword123!",
    )


    assert authenticated is not None
    assert authenticated["role"] == "investor"
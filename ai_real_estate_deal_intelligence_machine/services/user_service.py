from ai_real_estate_deal_intelligence_machine.auth.hashing import (
    hash_password,
    verify_password,
)

from ai_real_estate_deal_intelligence_machine.repositories.user_repository import (
    UserRepository,
)


class UserService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository


    def register_user(
        self,
        email: str,
        password: str,
        role: str = "investor",
    ):

        hashed_password = hash_password(password)

        return self.repository.create_user(
            {
                "email": email,
                "hashed_password": hashed_password,
                "role": role,
            }
        )


    def authenticate_user(
        self,
        email: str,
        password: str,
    ):

        user = self.repository.get_by_email(email)

        if not user:
            return None


        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None


        return user
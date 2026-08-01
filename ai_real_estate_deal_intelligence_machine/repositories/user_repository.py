from typing import Dict, Optional


class UserRepository:
    """
    Temporary in-memory user repository.

    This will later be replaced with the production database implementation.
    """

    def __init__(self):
        self.users: Dict[str, dict] = {}

    def create_user(self, user: dict) -> dict:
        self.users[user["email"]] = user
        return user

    def get_by_email(self, email: str) -> Optional[dict]:
        return self.users.get(email)
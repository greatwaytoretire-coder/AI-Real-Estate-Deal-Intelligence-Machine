from sqlalchemy.orm import Session

from ai_real_estate_deal_intelligence_machine.models.user import UserModel


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self,
        user_data: dict,
    ):
        user = UserModel(
            email=user_data["email"],
            hashed_password=user_data["hashed_password"],
            role=user_data.get("role", "investor"),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_email(
        self,
        email: str,
    ):
        return (
            self.db.query(UserModel)
            .filter(
                UserModel.email == email
            )
            .first()
        )
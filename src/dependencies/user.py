from dependencies.repo import get_user_repo
from services.user import UserService


def get_user_service() -> UserService:
    return UserService(
        user_repo=get_user_repo()
    )

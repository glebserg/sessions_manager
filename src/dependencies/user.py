from dependencies.repo import get_user_repo
from services.user import UserService


def get_user_service() -> UserService:
    """Возвращает сервис для работы с пользователями."""
    return UserService(user_repo=get_user_repo())

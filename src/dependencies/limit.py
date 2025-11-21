from dependencies.repo import get_limit_repo
from services.limit import LimitService


def get_limit_service() -> LimitService:
    """Возвращает Сервис для работы с лимитами."""
    return LimitService(limit_repo=get_limit_repo())

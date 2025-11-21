from dependencies.repo import get_limit_counter_repo
from services.limit_counter import LimitCounterService


def get_limit_counter_service() -> LimitCounterService:
    """Возвращает Сервис для работы со счётчиками лимитов."""
    return LimitCounterService(limit_counter_repo=get_limit_counter_repo())

from dependencies.repo import get_user_repo, get_limit_repo
from services.limit import LimitService


def get_limit_service() -> LimitService:
    return LimitService(
        limit_repo=get_limit_repo()
    )

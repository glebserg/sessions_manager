from dependencies.repo import get_app_repo
from services.app import AppService


def get_app_service() -> AppService:
    return AppService(
        app_repo=get_app_repo()
    )

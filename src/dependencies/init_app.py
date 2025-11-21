from typing import Optional

from constants import NAME_APP_SYSTEM
from dependencies.repo import get_app_repo, get_user_repo
from logger import uvicorn_logger
from models import AppModel, UserModel
from repositories.app import AppRepository
from repositories.user import UserRepository
from services.local_user_collector import LocalUserCollector
from shemes.app import CreateApp
from shemes.user import CreateUser, LocalUser


def create_system_app() -> None:
    """Добавляет 'системное' приложение."""
    repo_apps: AppRepository = get_app_repo()
    app_exist: Optional[AppModel] = repo_apps.get_by_name(NAME_APP_SYSTEM)
    if not app_exist:
        new_system_app = CreateApp(
            name=NAME_APP_SYSTEM,
            description="'Системное' приложение. "
            "Существует для глобальной блокировки доступа Пользователю(закрытия сессии)",
        )
        repo_apps.create(new_system_app)
        uvicorn_logger.info("'Системное' приложение добавлено в БД")


async def create_local_users_to_db() -> None:
    """Добавляет локального пользователя в БД."""
    collector = LocalUserCollector()
    local_users: list[LocalUser] = await collector.get_list()
    repo_users: UserRepository = get_user_repo()
    for local_user in local_users:
        user_exist: Optional[UserModel] = repo_users.get_by_username(local_user.username)
        if not user_exist:
            repo_users.create(CreateUser(**local_user.model_dump()))
            uvicorn_logger.info("Пользователь '{0}' добавлен в БД".format(local_user.username))

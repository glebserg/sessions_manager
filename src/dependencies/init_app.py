from typing import Optional

from constants import NAME_APP_SYSTEM
from database import engine, Base
from dependencies.repo import get_app_repo, get_user_repo
from logger import uvicorn_logger
from models import AppModel, UserModel
from repositories.app import AppRepository
from repositories.user import UserRepository
from services.local_user_collector import LocalUserCollector
from shemes.user import LocalUser, CreateUser


def create_base_app() -> None:
    repo_apps: AppRepository = get_app_repo()
    system_app: AppModel = repo_apps.get_or_create(NAME_APP_SYSTEM)
    if system_app[0]:
        uvicorn_logger.info("'Системное' приложение добавлено в БД")


def create_local_users_to_db(local_users: list[LocalUser]) -> None:
    repo_users: UserRepository = get_user_repo()
    for local_user in local_users:
        user_exist: Optional[UserModel] = repo_users.get_by_username(local_user.username)
        if not user_exist:
            repo_users.create(CreateUser(**local_user.model_dump()))
            uvicorn_logger.info("Пользователь '{0}' добавлен в БД".format(local_user.username))

async def init_app() -> None:
    Base.metadata.create_all(bind=engine)
    collector = LocalUserCollector()
    local_users: list[LocalUser] = await collector.get_list()
    create_local_users_to_db(local_users)
    create_base_app()
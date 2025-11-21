from datetime import datetime

from pydantic import BaseModel, computed_field

from services import get_count_today
from shemes import DBItemReader


class LocalUser(BaseModel):
    """Шаблон локального пользователя."""

    username: str


class CreateUser(BaseModel):
    """Форма добавления пользователя."""

    username: str


class UserList(DBItemReader):
    """Списочное представление пользователя."""

    id: int
    username: str


class UserAppLink(DBItemReader):
    """Приложение."""

    id: int
    name: str


class UserLimit(DBItemReader):
    """Лимит пользователя."""

    id: int
    app: UserAppLink
    minutes: int
    active: bool

    @computed_field
    def counter_today(self) -> int:
        """Счётчик за сегодня."""
        return get_count_today(self.id, datetime.today().date()) or 0


class UserDetail(UserList):
    """Детали пользователя."""

    created_at: datetime
    limits: list[UserLimit]

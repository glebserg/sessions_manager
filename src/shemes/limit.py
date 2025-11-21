from pydantic import BaseModel, Field

from shemes import DBItemReader
from shemes.app import AppDetail, AppList
from shemes.user import UserDetail, UserList


class CreateLimit(BaseModel):
    """Форма добавления лимита."""

    user_id: int = Field(ge=1)
    app_id: int = Field(ge=1)
    minutes: int = Field(ge=1, examples=[60])


class UpdateLimit(BaseModel):
    """Форма обновления лимита."""

    minutes: int = Field(ge=1, examples=[60])
    active: bool


class LimitList(DBItemReader):
    """Списочное представление лимита."""

    id: int
    minutes: int
    active: bool

    user: UserList
    app: AppList


class LimitDetail(LimitList):
    """Детали лимита."""

    user: UserDetail
    app: AppDetail

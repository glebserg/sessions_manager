from pydantic import BaseModel, Field

from shemes import DBItemReader
from shemes.app import AppList, AppDetail
from shemes.user import UserList, UserDetail


class CreateLimit(BaseModel):
    user_id: int = Field(ge=1)
    app_id: int = Field(ge=1)
    minutes: int = Field(ge=1, examples=[60])

class LimitList(DBItemReader):
    id: int
    minutes: int
    active: bool

    user: UserList
    app: AppList


class LimitDetail(LimitList):
    user: UserDetail
    app: AppDetail

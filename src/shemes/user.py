from datetime import datetime
from typing import Optional

from pydantic import BaseModel, computed_field

from services import get_count_today
from shemes import DBItemReader


class LocalUser(BaseModel):
    username: str


class CreateUser(BaseModel):
    username: str


class UserList(DBItemReader):
    id: int
    username: str


class App(DBItemReader):
    id: int
    name: str


class UserLimit(DBItemReader):
    id: int
    app: App
    minutes: int
    active: bool

    @computed_field
    def counter_today(self) -> int:
        return get_count_today(self.id, datetime.today().date()) or 0


class UserDetail(UserList):
    created_at: datetime
    limits: list[UserLimit]

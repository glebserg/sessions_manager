from datetime import datetime

from pydantic import BaseModel

from shemes import DBItemReader

class LocalUser(BaseModel):
    username: str

class CreateUser(BaseModel):
    username: str


class UserList(DBItemReader):
    id: int
    username: str


class UserDetail(UserList):
    created_at: datetime

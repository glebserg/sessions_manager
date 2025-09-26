from pydantic import BaseModel

from shemes import DBItemReader


class CreateApp(BaseModel):
    name: str

class AppList(DBItemReader):
    id:int
    name:str

class AppDetail(AppList):
    ...

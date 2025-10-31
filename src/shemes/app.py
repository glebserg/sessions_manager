from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from shemes import DBItemReader


class CreateApp(BaseModel):
    name: str
    description: Optional[str] = None

class AppList(DBItemReader):
    id:int
    name:str
    description: Optional[str] = None


class AppDetail(AppList):
    created_at: datetime


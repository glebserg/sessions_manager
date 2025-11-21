from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from shemes import DBItemReader


class CreateApp(BaseModel):
    """Форма добавления приложения."""

    name: str
    description: Optional[str] = None


class AppList(DBItemReader):
    """Списочное представление приложения."""

    id: int
    name: str
    description: Optional[str] = None


class AppDetail(AppList):
    """Детали приложения."""

    created_at: datetime

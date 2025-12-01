from datetime import datetime

from pydantic import BaseModel

from shemes import DBItemReader


class CreateApp(BaseModel):
    """Форма добавления приложения."""

    name: str
    description: str | None = None


class AppList(DBItemReader):
    """Списочное представление приложения."""

    id: int
    name: str
    description: str | None = None


class AppDetail(AppList):
    """Детали приложения."""

    created_at: datetime

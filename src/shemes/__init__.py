from abc import ABC

from pydantic import BaseModel


class DBItemReader(BaseModel, ABC):
    """Базовый абстрактный класс для сериализации Model в Pydantic."""

    class Config:
        from_attributes = True

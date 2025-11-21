from abc import ABC
from typing import Optional


class CustomError(Exception, ABC):
    """Базовое исключение с полем message."""

    message = "Something went wrong."

    def __init__(self, message: Optional[str] = None) -> None:
        if message is not None:
            self.message = message


class ObjectNotFoundError(CustomError):
    """Объект не найден."""

    def __init__(self, object_id: int, name: str = "Object"):
        super().__init__(f"{name} with id={object_id!s} not found")

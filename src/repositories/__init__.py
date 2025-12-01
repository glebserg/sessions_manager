from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import BaseIDModel


class BaseRepository(ABC):
    """Базовый репозиторий."""

    @property
    @abstractmethod
    def model(self) -> type[BaseIDModel]:
        """Префикс агента в etcd.

        Template:
            /{agent_key}/

        Example:
            /fc/

        """

    def __init__(self, db: Session):
        self._db = db

    def get_list(self, **filters: Any) -> list[type[BaseIDModel]]:
        """Список."""
        return list(self._db.query(self.model).filter_by(**filters).all())

    def get_by_id(self, pk: int) -> BaseIDModel | None:
        """Детали по id."""
        return self._db.query(self.model).get(pk)

    def get_first_or_none_by_filters(self, **filters: Any) -> BaseIDModel | None:
        """Детали по id."""
        return self._db.query(self.model).filter_by(**filters).first()

    def create(self, payload: BaseModel) -> BaseIDModel:
        """Добавить."""
        new_item = self.model(**payload.model_dump())
        self._db.add(new_item)
        self._db.commit()
        return new_item

    def delete(self, _id: int) -> None:
        """Удалить."""
        self._db.query(self.model).filter_by(id=_id).delete()
        self._db.commit()

    def save(self, item: BaseIDModel) -> None:
        """Сохранить."""
        self._db.add(item)
        self._db.commit()

from datetime import date
from typing import Optional

from models import LimitCounterModel
from repositories import BaseRepository


class LimitCounterRepository(BaseRepository):
    """Репозиторий счётчиков лимитов."""

    model = LimitCounterModel

    def get_list(self, limit_id: int | None = None) -> list[LimitCounterModel]:
        # TODO адаптировать под *args, **kwargs
        return self._db.query(LimitCounterModel).filter(LimitCounterModel.limit_id == limit_id).all()

    def get_or_none(self, limit_id: int, _date: date) -> Optional[LimitCounterModel]:
        """Получить, если есть."""
        return (
            self._db.query(LimitCounterModel)
            .filter(LimitCounterModel.limit_id == limit_id, LimitCounterModel.date == _date)
            .first()
        )

    def get_or_create(self, limit_id: int, _date: date) -> tuple[bool, LimitCounterModel]:
        """Получить и добавить, если не существует."""
        created: bool = False
        exist = self.get_or_none(limit_id, _date)
        if not exist:
            exist = LimitCounterModel(limit_id=limit_id, date=_date)
            self.save(exist)
        return created, exist

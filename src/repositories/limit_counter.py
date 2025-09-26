from datetime import date
from typing import Type, Optional

from repositories import BaseRepository
from models import LimitModel, LimitCounterModel
from shemes.limit import CreateLimit


class LimitCounterRepository(BaseRepository):

    def get_list(self, limit_id: int = None) -> list[LimitCounterModel]:
        return self._db.query(LimitCounterModel).filter(LimitCounterModel.limit_id == limit_id).all()

    def get_or_none(self, limit_id: int, _date: date) -> Optional[LimitCounterModel]:
        return (self._db.query(LimitCounterModel)
                .filter(LimitCounterModel.limit_id == limit_id)
                .first())

    def get_or_create(self, limit_id: int, _date: date) -> tuple[bool, Optional[LimitCounterModel]]:
        created: bool = False
        exist: Optional[LimitCounterModel] = self.get_or_none(limit_id, _date)
        if not exist:
            exist = LimitCounterModel(limit_id=limit_id,date=_date)
            self.save(exist)
        return created, exist

    def save(self, item: LimitCounterModel) -> None:
        self._db.add(item)
        self._db.commit()

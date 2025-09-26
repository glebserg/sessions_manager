from typing import Optional

from models import LimitCounterModel
from repositories.limit_counter import LimitCounterRepository
from shemes.limit_counter import LimitCounterList, LimitCounterDetail
from datetime import date


class LimitCounterService:

    def __init__(self, limit_counter_repo: LimitCounterRepository):
        self._limit_counter_repo = limit_counter_repo

    def get_list(self, limit_id: int = None) -> Optional[LimitCounterList]:
        return [LimitCounterList.model_validate(item) for item in self._limit_counter_repo.get_list(limit_id)]

    def get_or_none(self, limit_id: int, _date: date) -> Optional[LimitCounterDetail]:
        item: Optional[LimitCounterModel] = self._limit_counter_repo.get_or_none(limit_id, _date)
        if item:
            return LimitCounterDetail.model_validate(item)
        return None

    def counter_up(self, limit_id: int, _date: date) -> None:
        item: tuple[bool, Optional[LimitCounterModel]] = self._limit_counter_repo.get_or_create(limit_id, _date)
        item[1].count_minutes += 1
        self._limit_counter_repo.save(item[1])
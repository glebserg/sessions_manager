from datetime import date

from models import LimitCounterModel
from repositories.limit_counter import LimitCounterRepository
from shemes.limit_counter import LimitCounterDetail, LimitCounterList


class LimitCounterService:
    """Сервис для работы со счётчиками лимитов."""

    def __init__(self, limit_counter_repo: LimitCounterRepository):
        self._limit_counter_repo = limit_counter_repo

    def get_list(self, limit_id: int | None = None) -> list[LimitCounterList]:
        """Возвращает список счётчиков по лимиту."""
        return [LimitCounterList.model_validate(item) for item in self._limit_counter_repo.get_list(limit_id=limit_id)]

    def get_or_none(self, limit_id: int, _date: date) -> LimitCounterDetail | None:
        """Возвращает счётчик по лимиту и дате, если есть."""
        item: LimitCounterModel | None = self._limit_counter_repo.get_first_or_none_by_filters(
            limit_id=limit_id, date=_date
        )
        if item:
            return LimitCounterDetail.model_validate(item)
        return None

    def counter_up(self, limit_id: int, _date: date) -> None:
        """Увеличение счётчика на 1."""
        item: tuple[bool, LimitCounterModel] = self._limit_counter_repo.get_or_create(limit_id, _date)
        item[1].count_minutes += 1
        self._limit_counter_repo.save(item[1])

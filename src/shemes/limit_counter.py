from datetime import date

from shemes import DBItemReader


class LimitCounterList(DBItemReader):
    """Списочное представление счётчика лимита."""

    id: int
    limit_id: int
    count_minutes: int
    date: date


class LimitCounterDetail(LimitCounterList):
    """Детали счётчика лимита."""

    pass

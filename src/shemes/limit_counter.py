from datetime import date
from shemes import DBItemReader



class LimitCounterList(DBItemReader):
    id: int
    limit_id:int
    count_minutes: int
    date: date


class LimitCounterDetail(LimitCounterList):
    pass

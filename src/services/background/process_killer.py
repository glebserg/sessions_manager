from datetime import datetime,date
from typing import Optional

from services.limit import LimitService
from services.limit_counter import LimitCounterService
from services.processes_collector import ProcessesCollector
from shemes.proc import ActiveProcess


class ProcessKiller:
    def __init__(
            self,
            proc_collector: ProcessesCollector,
            limit_service: LimitService,
            limit_counter_service: LimitCounterService
    ) -> None:
        self._proc_collector = proc_collector
        self._limit_service = limit_service
        self._limit_counter_service = limit_counter_service

    def __call__(self) -> None:
        today: date = datetime.today()
        for limit in self._limit_service.get_list():
            if limit.active:
                coincidence: Optional[ActiveProcess] = self._proc_collector.get(limit.user.username, limit.app.name)
                if coincidence:
                    today_limit = self._limit_counter_service.get_or_none(limit_id=limit.id, _date=today)
                    print(today_limit)
                    # counter: LimitCounterModel = limit_counter_service.get(limit.id, today)
                    # if counter.count_minutes >= limit.minutes:
                    #     await run_cmd(f"kill {coincidence.pid}")

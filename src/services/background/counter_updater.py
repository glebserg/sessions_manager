from datetime import datetime, date
from typing import Optional

from constants import NAME_APP_SYSTEM
from services.limit import LimitService
from services.limit_counter import LimitCounterService
from services.processes_collector import ProcessesCollector
from services.sessions_collector import SessionsCollector
from shemes.proc import ActiveProcess


class CounterUpdater:

    def __init__(
            self,
            proc_collector: ProcessesCollector,
            session_collector: SessionsCollector,
            limit_service: LimitService,
            limit_counter_service: LimitCounterService
    ) -> None:
        self._proc_collector = proc_collector
        self._session_collector = session_collector
        self._limit_service = limit_service
        self._limit_counter_service = limit_counter_service

    async def __call__(self) -> None:
        today: date = datetime.today().date()
        for limit in self._limit_service.get_list():
            if limit.active:
                if self._proc_collector.get(limit.user.username, limit.app.name):
                    self._limit_counter_service.counter_up(limit.id, today)

                if self._session_collector.is_active(limit.user.username) and limit.app.name == NAME_APP_SYSTEM:
                    self._limit_counter_service.counter_up(limit.id, today)

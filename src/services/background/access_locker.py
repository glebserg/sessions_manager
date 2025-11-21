from datetime import date, datetime
from typing import Final, Optional

from constants import NAME_APP_SYSTEM
from logger import uvicorn_logger
from services.limit import LimitService
from services.limit_counter import LimitCounterService
from services.processes_collector import ProcessesCollector
from services.sessions_collector import SessionsCollector
from shemes.cli import CLIResult
from shemes.limit_counter import LimitCounterDetail
from utils.cmd import run_cmd


class AccessLocker:
    """Блокиратор доступа."""

    __CMD_KILL_SESSION: Final[str] = "pkill -u {username}"
    __CMD_KILL_PROCESS: Final[str] = __CMD_KILL_SESSION + " {process_name}"

    def __init__(
        self,
        proc_collector: ProcessesCollector,
        session_collector: SessionsCollector,
        limit_service: LimitService,
        limit_counter_service: LimitCounterService,
    ) -> None:
        self._proc_collector = proc_collector
        self._session_collector = session_collector
        self._limit_service = limit_service
        self._limit_counter_service = limit_counter_service

    async def __get_cmd(self, username: str, process_name: str) -> str:
        if process_name == NAME_APP_SYSTEM:
            return self.__CMD_KILL_SESSION.format(username=username)
        else:
            return self.__CMD_KILL_PROCESS.format(username=username, process_name=process_name)

    async def __kill_process(self, username: str, process_name: str) -> None:
        cmd: str = self.__CMD_KILL_PROCESS.format(username=username, process_name=process_name)
        res: CLIResult = await run_cmd(cmd)
        if res.status_code == 0:
            uvicorn_logger.debug(f"Killed the process '{process_name}' for user '{username}'")
        else:
            uvicorn_logger.error(f"CMD: {cmd} . Status code: {res.status_code}. MSG: {res.stderr}")

    async def __kill_session(self, username: str) -> None:
        cmd: str = self.__CMD_KILL_SESSION.format(username=username)
        res: CLIResult = await run_cmd(cmd)
        if res.status_code == 0:
            uvicorn_logger.debug(f"Killed the session for user '{username}'")
        else:
            uvicorn_logger.error(f"CMD: {cmd} . Status code: {res.status_code}. MSG: {res.stderr}")

    async def __call__(self) -> None:
        """Вызов."""
        today: date = datetime.today().date()
        for limit in self._limit_service.get_list():
            if limit.active:
                if self._proc_collector.get(limit.user.username, limit.app.name):
                    today_limit: Optional[LimitCounterDetail] = self._limit_counter_service.get_or_none(
                        limit_id=limit.id, _date=today
                    )
                    if today_limit and today_limit.count_minutes >= limit.minutes:
                        await self.__kill_process(limit.user.username, limit.app.name)
                if limit.app.name == NAME_APP_SYSTEM and self._session_collector.is_active(limit.user.username):
                    await self.__kill_session(limit.user.username)

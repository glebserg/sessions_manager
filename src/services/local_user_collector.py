from shemes.user import LocalUser
from shemes.cli import CLIResult
from utils.checks import CheckData
from utils.cmd import run_cmd


class LocalUserCollector:

    def __init__(self) -> None:
        self.__updated: bool = False
        self._local_users: list[LocalUser] = []

    def __is_service_user(self) -> bool:
        pass

    def __is_valid_user(self, raw_data: str) -> bool:
        for checker_cls in CheckData.__subclasses__():
            checker = checker_cls(raw_data)
            if not checker.passed():
                return False
        return True

    def __parse_users(self, raw_data: str) -> list[LocalUser]:
        return [
            LocalUser(username=line.split(":")[0])
            for line in raw_data.splitlines()
            if self.__is_valid_user(line)
        ]

    async def _update(self) -> None:
        result: CLIResult = await run_cmd("cat /etc/passwd")
        if result.status_code == 0:
            self._local_users =  self.__parse_users(result.stdout)

    async def get_list(self) -> list[LocalUser]:
        if not self.__updated:
            await self._update()
        return self._local_users

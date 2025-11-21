from shemes.cli import CLIResult
from shemes.user import LocalUser
from utils.checks import CheckRawUser
from utils.cmd import run_cmd


class LocalUserCollector:
    """Собиратель локальных пользователей."""

    def __init__(self) -> None:
        self.__updated: bool = False
        self._local_users: list[LocalUser] = []

    def __is_valid_user(self, raw_data: str) -> bool:
        return all(checker_cls(raw_data).passed() for checker_cls in CheckRawUser.__subclasses__())

    def __parse_users(self, raw_data: str) -> list[LocalUser]:
        return [LocalUser(username=line.split(":")[0]) for line in raw_data.splitlines() if self.__is_valid_user(line)]

    async def _update(self) -> None:
        """Обновить."""
        result: CLIResult = await run_cmd("cat /etc/passwd")
        if result.status_code == 0:
            self._local_users = self.__parse_users(result.stdout)

    async def get_list(self) -> list[LocalUser]:
        """Возвращает список пользователей."""
        if not self.__updated:
            await self._update()
        return self._local_users

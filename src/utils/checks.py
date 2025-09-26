from abc import ABC, abstractmethod


class CheckData(ABC):

    def __init__(self, raw_data: str) -> None:
        self._raw_data = raw_data

    @abstractmethod
    def passed(self) -> bool:
        """Проверка."""


class NoLogin(CheckData):
    def passed(self) -> bool:
        return "/usr/sbin/nologin" not in self._raw_data


class BinFalse(CheckData):
    def passed(self) -> bool:
        return "/bin/false" not in self._raw_data


class BinSync(CheckData):
    def passed(self) -> bool:
        return "/bin/sync" not in self._raw_data

class NoRootUser(CheckData):
    def passed(self) -> bool:
        return not self._raw_data.startswith("root")

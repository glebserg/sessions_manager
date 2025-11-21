from abc import ABC, abstractmethod


class CheckRawUser(ABC):
    """Проверка сырых данных о пользователе."""

    def __init__(self, raw_data: str) -> None:
        self._raw_data = raw_data

    @abstractmethod
    def passed(self) -> bool:
        """Проверка."""


class NoLogin(CheckRawUser):
    """Проверка отсутствия системной учетной записи с nologin."""

    def passed(self) -> bool:
        """Проверка."""
        return "/usr/sbin/nologin" not in self._raw_data


class BinFalse(CheckRawUser):
    """Проверка отсутствия системной учетной записи с /bin/false."""

    def passed(self) -> bool:
        """Проверка."""
        return "/bin/false" not in self._raw_data


class BinSync(CheckRawUser):
    """Проверка отсутствия системной учетной записи sync."""

    def passed(self) -> bool:
        """Проверка."""
        return "/bin/sync" not in self._raw_data


class NoRootUser(CheckRawUser):
    """Проверка что пользователь не является root."""

    def passed(self) -> bool:
        """Проверка."""
        return not self._raw_data.startswith("root")

import psutil

from shemes.session import ActiveSession


class SessionsCollector:
    """Собиратель сессий пользователей."""

    def __init__(self) -> None:
        self.__updated: bool = False
        self._active_sessions: list[ActiveSession] = []

    def update(
        self,
    ) -> None:
        """Обновление."""
        for user_session in psutil.users():
            self._active_sessions.append(ActiveSession.model_validate(user_session))

    def is_active(self, username: str) -> bool:
        """Возвращает статус активности пользователя в текущий момент."""
        if not self.__updated:
            self.update()
        return username in [session.name for session in self._active_sessions]

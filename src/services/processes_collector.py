import psutil

from shemes.proc import ActiveProcess


class ProcessesCollector:
    """Собиратель процессов Операционной Системы."""

    def __init__(self) -> None:
        self.__updated: bool = False
        self._active_processes: list[ActiveProcess] = []

    def update(
        self,
    ) -> None:
        """Обновить."""
        for proc in psutil.process_iter(["username", "name", "pid"]):
            try:
                self._active_processes.append(ActiveProcess(**proc.info))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def get(self, username: str, app_name: str) -> ActiveProcess | None:
        """Получить."""
        if not self.__updated:
            self.update()
        for active_proc in self._active_processes:
            if active_proc.username == username and active_proc.name == app_name:
                return active_proc
        return None

from pydantic_settings import BaseSettings
from starlette.templating import Jinja2Templates


class AppSettings(BaseSettings):
    """Настройки приложения."""

    DEV: bool = False
    LOG_LEVEL: str = "INFO"
    PORT: int = 5000


class DatabaseSettings(AppSettings):
    """Настройки БД."""

    DB_NAME: str = "session-manager.db"

    @property
    def DB_URL(self) -> str:
        """Путь к БД."""
        return f"sqlite:///../{self.DB_NAME}" if self.DEV else f"sqlite:///./{self.DB_NAME}"


app_setting = AppSettings()
database_settings = DatabaseSettings()
templates = Jinja2Templates(directory="templates")

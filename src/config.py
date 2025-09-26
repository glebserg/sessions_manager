from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    DEV: bool = False
    LOG_LEVEL: str = "INFO"
    PORT: int


class DatabaseSettings(BaseSettings):
    DB_NAME: str = ""

    @property
    def DB_URL(self) -> str:
        # return f"sqlite:///../{self.DB_NAME}"
        return f"sqlite+aiosqlite:///../{self.DB_NAME}"


app_setting = AppSettings()
database_settings = DatabaseSettings()
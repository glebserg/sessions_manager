from pydantic import BaseModel


class CLIResult(BaseModel):
    """Результат выполнения команды CLI."""

    status_code: int
    stdout: str
    stderr: str

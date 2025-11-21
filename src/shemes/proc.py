from pydantic import BaseModel


class ActiveProcess(BaseModel):
    """Активный процесс."""

    pid: int
    name: str
    username: str

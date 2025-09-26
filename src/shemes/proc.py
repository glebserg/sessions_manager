from pydantic import BaseModel


class ActiveProcess(BaseModel):
    pid: int
    name: str
    username: str
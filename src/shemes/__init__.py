from pydantic import BaseModel


class DBItemReader(BaseModel):
    class Config:
        from_attributes = True
from pydantic import BaseModel


class ServerErrorSchema(BaseModel):
    code: int
    detail: str

from .base import Field, CamelModel


class MessageOk(CamelModel):
    msg: str = Field(default="OK")

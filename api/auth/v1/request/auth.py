from typing import Optional
from pydantic import Field

from core.fastapi.schemas.base import CamelModel


class GoogleLoginRequest(CamelModel):
    id_token: str = Field(None)
    language: Optional[str] = Field(None)
    region: Optional[str] = Field(None)
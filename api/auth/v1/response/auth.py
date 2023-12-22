from pydantic import Field
from core.fastapi.schemas.base import CamelModel


class TokenResponse(CamelModel):
    access_token: str = Field(None, example="{access_token}")
    refresh_token: str = Field(None, example="{refresh_token}")

class GoogleTokenResponse(TokenResponse):
    user_id: str = Field(None, nullabe=False, example="{uuid}")
    picture_url: str = Field(None, example="https://picture.png")
    nick_name: str = Field(None, nullable=True, example="seokjohn")
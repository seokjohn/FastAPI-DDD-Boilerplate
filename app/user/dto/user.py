from datetime import datetime
from pydantic import BaseModel, Field
from core.fastapi.schemas.base import InfoModel, CamelModel

from app.user.enums import (
    SnsType,
    UserStatus
)

class UserToken(BaseModel):
    id: str = Field(example="{uuid}")
    email: str = Field(None, example="angryong@lionrocket.ai")
    sns_type: str = Field(None, example=SnsType.email)
    status: str = Field(None, example=UserStatus.active)

    class Config:
        orm_mode = True

class ProfileInfo(InfoModel):
    id: str = Field(example="{uuid}")
    user_id: str = Field(None, nullabe=False, example="{uuid}")
    picture_url: str = Field(None, example="https://picture.png")
    nick_name: str = Field(None, nullable=True, example="seokjohn")

    class Config:
        orm_mode = True


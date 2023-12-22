from typing import Optional

from sqlalchemy import select

from app.user.entity import Profiles
from core.db import session
from core.repository.base import CRUDRepository


class ProfileRepository(CRUDRepository[Profiles, str]):
    async def find_by_user_id(self, user_id: str) -> Optional[Profiles]:
        query = select(self.model).where(self.model.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_by_query(self, query):
        result = await session.execute(query)
        return result.scalars()

    async def search_all_by_keyword(self, keyword, limit: int = 50):
        query = select(self.model).where(self.model.nick_name == keyword).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


profile_repository = ProfileRepository(Profiles)
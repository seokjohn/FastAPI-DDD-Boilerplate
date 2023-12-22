from sqlalchemy import select

from app.user.entity import Users
from core.db import session
from core.repository.base import CRUDRepository


class UserRepository(CRUDRepository[Users, str]):
    async def find_by_id_and_email(self, id: str, email: str):
        query = select(self.model).where(self.model.id == id, self.model.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_by_query(self, query):
        result = await session.execute(query)
        return result.scalars()


user_repository = UserRepository(Users)

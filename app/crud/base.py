from typing import Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base import Base
from app.models import User


ModelType = TypeVar('ModelType', bound=Base)


def get_diff_or_zero(a, b):
    """Функция возвращающая разницу или ноль"""
    # Used for investition in order you cannot invest more money than a project needs
    return int(((a - b) + abs(a - b)) / 2)


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            # schema instance
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            # add user to dict with fields values if needed
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_id_by_name(
            self,
            name: str,
            model: Type[ModelType],
            session: AsyncSession,
    ) -> Optional[int]:
        db_id = await session.execute(
            select(model.id).where(
                model.name == name
            )
        )
        db_id = db_id.scalars().first()
        return db_id

    async def get_by_user(
            self,
            model: Type[ModelType],
            session: AsyncSession,
            user: User
    ):
        objects = await session.execute(
            select(model).where(
                model.user_id == user.id
            )
        )
        return objects.scalars().all()

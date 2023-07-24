from typing import TypeVar, Type

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.core.base import Base

ModelType = TypeVar('ModelType', bound=Base)
CrudType = TypeVar('CrudType', bound=CRUDBase)
SchemaType = TypeVar('SchemaType', bound=BaseModel)
# this annotation means that annoted variable will be class
# inherited from bound


async def check_name_duplicate(
        object_name: str,
        model: Type[ModelType],
        # instance of class inherited from bound
        crud_object: CrudType,
        session: AsyncSession,
) -> None:
    object_id = await crud_object.get_id_by_name(object_name, model, session)
    if object_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_object_exists(
        id: int,
        crud_object: CrudType,
        session: AsyncSession,
) -> ModelType:
    object = await crud_object.get(id, session)
    # will be donation_crud or charity_crud depending on in which router it is used
    if object is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден'
        )
    return object


def check_before_edit(
        object: ModelType,
        obj_in: Type[SchemaType],
) -> ModelType:
    if object.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    if obj_in.full_amount is not None:
        if object.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=422,
                detail='Полная сумма не может быть меньше уже внесенной суммы'
            )
    return object


def check_invested(
    object: ModelType,
) -> ModelType:
    if object.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return object
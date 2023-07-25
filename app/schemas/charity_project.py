from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, root_validator

from app.schemas.base import ProjectDonationSchemaBase, ProjectDonationSchemaDB


class CharityProjectBase(ProjectDonationSchemaBase):
    name: str = Field(..., min_length=1, max_length=100, example="project1")
    description: str = Field(..., min_length=1, example="description")

    @root_validator
    def check_fields(cls, values):
        if (
            "full_amount" not in values
            or "name" not in values
            or "description" not in values
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Заполните, пожалуйста, все обязательные поля",
            )
        return values


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    full_amount: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, min_length=1, max_length=100, example="project1")
    description: Optional[str] = Field(None, min_length=1, example="description")

    @root_validator
    def check_fields(cls, values):
        if (
            "full_amount" not in values
            and "name" not in values
            and "description" not in values
        ):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Для обновления проекта необходимо заполнить хотя бы одно поле",
            )
        return values

    class Config:
        extra = "forbid"


class CharityProjectDB(CharityProjectBase, ProjectDonationSchemaDB):
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

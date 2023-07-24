from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.base import ProjectDonationSchemaBase, ProjectDonationSchemaDB


class CharityProjectBase(ProjectDonationSchemaBase):
    name: str = Field(..., min_length=1, max_length=100, example='project1')
    description: str = Field(..., min_length=1, example='description')


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    full_amount: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, min_length=1, max_length=100, example='project1')
    description: Optional[str] = Field(None, min_length=1, example='description')

    class Config:
        extra = "forbid"


class CharityProjectDB(CharityProjectBase, ProjectDonationSchemaDB):
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

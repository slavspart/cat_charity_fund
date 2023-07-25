from datetime import datetime
from typing import Optional

from pydantic import Field

from app.schemas.base import ProjectDonationSchemaBase, ProjectDonationSchemaDB


class DonationBase(ProjectDonationSchemaBase):
    comment: Optional[str] = Field(None, min_length=1, example="comment")


class DonationCreate(DonationBase):
    pass


class DonationDB_short(DonationBase, ProjectDonationSchemaDB):
    id: int


class DonationDB_long(DonationDB_short):
    user_id: int
    invested_amount: int
    fully_invested: bool
    сlose_date: Optional[datetime]

from datetime import datetime

from pydantic import BaseModel, Extra, Field


class ProjectDonationSchemaBase(BaseModel):
    full_amount: int = Field(..., gt=0)


class ProjectDonationSchemaDB(ProjectDonationSchemaBase):
    id: int
    create_date: datetime
    # Every api response contains at least 3 fields (id, full_amount , create_date)

    class Config:
        orm_mode = True
        # schema receives model instance from db and serialize it
        extra = Extra.forbid
        # you cannot transfer field which are not in schema

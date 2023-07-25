from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(
        Text,
    )
    full_amount = Column(Integer(), nullable=False)
    invested_amount = Column(Integer(), nullable=False, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __str__(self):
        return f"Проект {self.id}"

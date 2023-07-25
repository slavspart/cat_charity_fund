from datetime import datetime

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    # each model will have id field
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        # Each table will have name as the name of model
        return cls.__name__.lower()

    def close(self):
        print(self, self.full_amount, self.invested_amount)
        if self.full_amount == self.invested_amount:
            self.fully_invested = True
            self.close_date = datetime.now()


# Prebase will be used for each table
Base = declarative_base(cls=PreBase)


engine = create_async_engine(settings.database_url)
# engine to connect db
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
# function to generate sessions


async def get_async_session():
    # function to get session where needed
    async with AsyncSessionLocal() as async_session:
        yield async_session
        # means that session will be closed when request is sent
        # but will be able to get another session when need
        # if it is return instead of yield the function will stop to receive sessions

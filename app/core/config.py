from pydantic import BaseSettings


class Settings(BaseSettings):
    # if there is same value in env it will be used
    app_title: str = 'Кошачий благотворительный фонд (0.1.0)'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
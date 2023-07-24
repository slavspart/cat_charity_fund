from pydantic import BaseSettings


class Settings(BaseSettings):
    # if there is same value in env it will be used
    app_title: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
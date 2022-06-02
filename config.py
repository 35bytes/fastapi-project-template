import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str = os.getenv("SECRET")
    db_dialect: str = os.getenv("DB_DIALECT")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

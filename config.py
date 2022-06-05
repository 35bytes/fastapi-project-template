import os
from functools import lru_cache
from pydantic import BaseSettings


####### Settings #######

class Settings(BaseSettings):
    env_mode: str = os.getenv("SECRET")
    secret: str = os.getenv("SECRET")
    db_dialect: str = os.getenv("DB_DIALECT")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")
    db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()


####### Database #######

@lru_cache()
def get_db_url(test_mode: bool=get_settings().env_mode == "test") -> str:
    if test_mode:
        return "sqlite://"
    settings = get_settings()
    return f"{settings.db_dialect}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

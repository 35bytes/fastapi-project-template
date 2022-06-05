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

    def __hash__(self):
        return hash(tuple(self))


def get_settings() -> Settings:
    return Settings()


####### Database #######

@lru_cache()
def get_db_url(settings: Settings=get_settings()) -> str:
    if settings.env_mode == "test":
        return "sqlite://"
    return f"{settings.db_dialect}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    secret: str = os.getenv("SECRET")
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

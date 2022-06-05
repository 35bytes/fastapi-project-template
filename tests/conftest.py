import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine

from config import Settings, get_settings, get_db_url
from src.adapters.orm import Base


@pytest.fixture(scope="module")
def load_env_variables():
    load_dotenv()


@pytest.fixture(scope="session")
def config_test() -> Settings:
    os.environ["ENV_MODE"] = "test"
    settings = get_settings(test_mode=True)
    return settings


@pytest.fixture(scope="session")
def create_db_in_memory(config_test):
    engine = create_engine(get_db_url(settings=config_test))
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

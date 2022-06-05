import os
import pytest
from dotenv import load_dotenv

from config import Settings, get_settings


@pytest.fixture(scope="module")
def load_env_variables():
    load_dotenv()


@pytest.fixture(scope="session")
def config_test() -> Settings:
    os.environ["ENV_MODE"] = "test"
    settings = get_settings()
    return settings

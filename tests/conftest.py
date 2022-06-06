import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from fastapi.testclient import TestClient

from config import Settings, get_settings, get_db_url
from src.adapters.orm import Base
from src.entrypoints.main import app


@pytest.fixture
def load_env_variables():
    load_dotenv()


@pytest.fixture
def client():
    return TestClient(app)

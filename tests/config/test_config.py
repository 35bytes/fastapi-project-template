import os
from config import get_settings, get_db_url


def test_config_values():
    settings = get_settings()
    assert settings.secret == os.getenv("SECRET")
    assert settings.db_dialect == os.getenv("DB_DIALECT")
    assert settings.db_host == os.getenv("DB_HOST")
    assert settings.db_port == os.getenv("DB_PORT")
    assert settings.db_name == os.getenv("DB_NAME")
    assert settings.db_user == os.getenv("DB_USER")
    assert settings.db_password == os.getenv("DB_PASSWORD")


def test_db_url():
    expected = f"{os.getenv('DB_DIALECT')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    assert get_db_url() == expected

import pytest
from pydantic.error_wrappers import ValidationError
from src.domain.schemas import UserBase, UserCreate


def test_valid_user_base():
    user_base = UserBase(email="test@123.cl")
    assert user_base.email == "test@123.cl"


def test_not_valid_email_in_user_base():
    with pytest.raises(ValidationError):
        UserBase(email="test123.cl")


def test_valid_user_create():
    user_create = UserCreate(email="test@123.cl", password="123", password2="123")
    assert user_create.email == "test@123.cl"
    assert user_create.password == "123"
    assert user_create.password2 == "123"


def test_not_valid_email_in_user_create():
    with pytest.raises(ValidationError):
        UserCreate(email="test123.cl", password="123", password2="123")

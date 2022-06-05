import pytest
from pydantic.error_wrappers import ValidationError
from src.domain.schemas import UserBase, UserCreate


def test_valid_user_base():
    user_base = UserBase(email="karl@123.cl")
    assert user_base.email == "karl@123.cl"


def test_not_valid_email_in_user_base():
    with pytest.raises(ValidationError):
        UserBase(email="karl123.cl")


def test_valid_user_create():
    user_create = UserCreate(email="karl@123.cl", password="123", password2="123")
    assert user_create.email == "karl@123.cl"
    assert user_create.password == "123"
    assert user_create.password2 == "123"


def test_not_valid_email_in_user_create():
    with pytest.raises(ValidationError):
        UserCreate(email="karl123.cl", password="123", password2="123")

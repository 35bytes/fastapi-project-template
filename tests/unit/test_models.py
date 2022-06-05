from src.domain.models import User


def test_user_model():
    user = User(id=1, email="test@123.cl", hashed_password="123")
    assert user.id == 1
    assert user.email == "test@123.cl"
    assert user.hashed_password == "123"

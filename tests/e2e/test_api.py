# System
import sys
import pathlib

# Packages
from fastapi.testclient import TestClient

# Set root path
PACKAGE_PARENT = pathlib.Path(__file__).parents[2]
sys.path.append(str(PACKAGE_PARENT))

# Import other modules
from src.entrypoints.main import app


client = TestClient(app)


def test_create_user():
    body={
        "email": "test@123.cl",
        "password": "123456", 
        "password2": "123456"
    }

    response = client.post("/", json=body)
    assert response.status_code == 201
    assert response.json() == {"email": "test@123.cl"}


def test_fail_create_user_because_password_dont_match():
    body={
        "email": "test@123.cl",
        "password": "123456",
        "password2": "1234567"
    }

    response = client.post("/", json=body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Passwords don't match"}


def test_fail_because_email_is_not_valid():
    body={
        "email": "test",
        "password": "123456", 
        "password2": "123456"
    }

    response = client.post("/", json=body)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid email address"

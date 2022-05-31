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


def test_hello_worl():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_user(client):
    body={
        "email": "test@123.cl",
        "password": "123456", 
        "password2": "123456"
    }

    response = client.post("/", json=body)
    assert response.status_code == 201
    assert response.json() == {"email": "test@123.cl"}


def test_user_already_exist(client):
    body={
        "email": "test@123.cl",
        "password": "123456", 
        "password2": "123456"
    }
    response = client.post("/", json=body)
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_password_dont_match(client):
    body={
        "email": "test@123.cl",
        "password": "123456", 
        "password2": "1234567"
    }
    response = client.post("/", json=body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Passwords don't match"}

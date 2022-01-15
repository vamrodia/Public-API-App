# Created to make the fixtures available to all the tests modules
# Modules/Library Imports and initialization

from app import schemas
from jose import jwt
from app.config import settings
import pytest


# Function to test the Root Path
# def test_root(client):
#     res = client.get("/")
#     # print(res.json().get('message'))
#     assert res.json().get('message') == "Welcome to this Basic API Application created by Vibhor Amrodia"
#     assert res.status_code == 200


# Function to test the "Create Users" path
def test_create_user(client):
    res = client.post("/users/create", json={"email": "hello123@gmail.com", "password": "password"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


# Function to test the "Login Users" path
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    # print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    user_identity: str = payload.get("user_id")
    assert user_identity == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@user.com', 'testpass', 403),
    ('testvibhor@user.com', 'wrongpassword', 403),
    ('wrongemail@user.com', 'wrongpassword', 403),
    (None, 'testpass', 422),
    ('testvibhor@user.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'

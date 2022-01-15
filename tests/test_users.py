from app import schemas
from .database import client, session


# Function to test the Root Path
def test_root(client):
    res = client.get("/")
    # print(res.json().get('message'))
    assert res.json().get('message') == "Welcome to this Basic API Application created by Vibhor Amrodia"
    assert res.status_code == 200


# Function to test the "Create Users" path
def test_create_user(client):
    res = client.post("/users/create", json={"email": "hello123@gmail.com", "password": "password"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

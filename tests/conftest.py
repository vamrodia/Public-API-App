# Modules/Library Imports and initialization
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from urllib.parse import quote
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
import pytest

# Defining the MySQL URL and connecting the the Database
pgsql_url = f"postgresql+psycopg2://{settings.database_username}" \
            f":%s@{settings.database_hostname}:{settings.database_port}" \
            f"/{settings.database_name}_test" % quote(settings.database_password)

engine = create_engine(pgsql_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")  # This to run the fixture for every test
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Calling the FastAPI App and initializing it
@pytest.fixture(scope="function")  # This to run the fixture for every test
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# Creating a Test user using a Fixture to be referenced by other tests
@pytest.fixture()
def test_user2(client):
    user_data = {"email": "testvibhor2@user.com",
                 "password": "testpass"}
    res = client.post("/users/create", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


# Creating a Test user using a Fixture to be referenced by other tests
@pytest.fixture()
def test_user(client):
    user_data = {"email": "testvibhor@user.com",
                 "password": "testpass"}
    res = client.post("/users/create", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


# Creating a Token to be used as a Fixture and will be referenced by other tests
@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


# Creating an authorized user to be used as a Fixture and will be referenced by other tests
@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# Creating test posts to be used as a Fixture and will be referenced by other tests
@pytest.fixture()
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "First Title",
        "content": "First Content",
        "owner_id": test_user['id']
    }, {
        "title": "Second Title",
        "content": "Second Content",
        "owner_id": test_user['id']
    }, {
        "title": "Third Title",
        "content": "Third Content",
        "owner_id": test_user['id']
    }, {
        "title": "Third Title",
        "content": "Third Content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts

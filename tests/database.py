# Modules/Library Imports and initialization
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from urllib.parse import quote
from app.database import get_db, Base
import pytest

# Defining the MySQL URL and connecting the the Database
pgsql_url = f"postgresql+psycopg2://{settings.database_username}" \
            f":%s@{settings.database_hostname}:{settings.database_port}" \
            f"/{settings.database_name}_test" % quote(settings.database_password)

engine = create_engine(pgsql_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Calling the FastAPI App and initializing it
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
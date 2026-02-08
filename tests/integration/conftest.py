import os

os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["JWT_SECRET_KEY"] = "super_secure_test_secret_key_that_is_long_enough_for_sha256"

import pytest
import uuid
from src.app.app import create_app
from src.app.externals.db.connection import engine, SessionLocal
from src.app.externals.models.base import Base
from src.app.externals.models.user import User
from src.app.security.jwt_utils import create_token


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@pytest.fixture
def test_app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def test_user(db):
    user = User(
        name="Test pytest User",
        email=f"test_{uuid.uuid4()}@example.com",
        password="123456"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    token = create_token(str(test_user.id))
    return {"Authorization": f"Bearer {token}"}

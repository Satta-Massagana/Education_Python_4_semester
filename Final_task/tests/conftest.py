import pytest
import uuid
from passlib.context import CryptContext
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db.db_conf import Base, get_db
from db.models.user_model import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def test_app():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def db_session(test_app):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def auth_headers(test_app, db_session):
    """Fixture to get authenticated headers with valid password hash"""

    unique_id = str(uuid.uuid4())[:8]
    email = f"test{unique_id}@example.com"
    login = f"testuser{unique_id}"

    password_hash = pwd_context.hash("test")

    user = User(
        first_name="Test",
        last_name="User",
        login=login,
        email=email,
        password_hash=password_hash,
        created_at=datetime.utcnow(),
        active=True
    )
    db_session.add(user)
    db_session.commit()

    login_data = {
        "username": login,
        "password": "test"
    }

    response = test_app.post("/auth/login", data=login_data)
    token = response.json()["access_token"]

    return {"header": { "Authorization": f"Bearer {token}" }, "user_id": user.id}
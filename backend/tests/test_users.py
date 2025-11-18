from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pytest

from backend.database import Base
from backend.main import app, get_db, pwd_context # Импортируем pwd_context
from backend import models, schemas, crud

# Setup for test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine) # Drop tables after tests

@pytest.fixture(name="client")
def client_fixture(db_session: Session): # Зависимость от db_session
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = {}


# --- User Endpoints Tests ---
def test_create_user(client: TestClient, db_session: Session):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "shortpass",
        "role": "engineer"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"
    assert response.json()["role"] == "engineer"

def test_create_user_duplicate_email(client: TestClient, db_session: Session):
    user_data = {
        "username": "user1",
        "email": "duplicate@example.com",
        "password": "shortpass",
        "role": "engineer"
    }
    client.post("/users/", json=user_data)
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]

def test_create_user_duplicate_username(client: TestClient, db_session: Session):
    user_data = {
        "username": "duplicateuser",
        "email": "unique@example.com",
        "password": "shortpass",
        "role": "engineer"
    }
    client.post("/users/", json=user_data)
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]

def test_login_for_access_token(client: TestClient, db_session: Session):
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "testpass",
        "role": "engineer"
    }
    client.post("/users/", json=user_data)

    form_data = {"username": "loginuser", "password": "testpass"}
    response = client.post("/token", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_invalid_password(client: TestClient, db_session: Session):
    user_data = {
        "username": "invalidpassuser",
        "email": "invalidpass@example.com",
        "password": "testpass",
        "role": "engineer"
    }
    client.post("/users/", json=user_data)

    response = client.post(
        "/token",
        data={
            "username": user_data["username"],
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_read_users_me(client: TestClient, db_session: Session):
    user_data = {
        "username": "meuser",
        "email": "me@example.com",
        "password": "testpass",
        "role": "manager"
    }
    client.post("/users/", json=user_data)

    form_data = {"username": "meuser", "password": "testpass"}
    token_response = client.post("/token", data=form_data)
    token = token_response.json()["access_token"]

    response = client.get("/users/me/", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"

def test_read_user_by_id(client: TestClient, db_session: Session):
    user_data = {
        "username": "userbyid",
        "email": "userbyid@example.com",
        "password": "testpass",
        "role": "engineer"
    }
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    form_data = {"username": "userbyid", "password": "testpass"}
    token_response = client.post("/token", data=form_data)
    token = token_response.json()["access_token"]

    response = client.get(f"/users/{user_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "userbyid"

def test_read_nonexistent_user_by_id(client: TestClient, db_session: Session):
    user_data = {
        "username": "reader",
        "email": "reader@example.com",
        "password": "testpass",
        "role": "engineer"
    }
    client.post("/users/", json=user_data)

    form_data = {"username": "reader", "password": "testpass"}
    token_response = client.post("/token", data=form_data)
    token = token_response.json()["access_token"]

    response = client.get(f"/users/999", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

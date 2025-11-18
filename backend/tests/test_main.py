import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..main import app, get_db
from ..database import Base
from .. import models, schemas, crud
from passlib.context import CryptContext
import random # Добавляем импорт random

# Setup for test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Password hashing context for tests
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="test_user_create")
def test_user_create_fixture():
    unique_id = random.randint(1, 100000)
    return schemas.UserCreate(username=f"testuser_{unique_id}", email=f"test_{unique_id}@example.com", password="shortpass", role="engineer")

@pytest.fixture(name="test_user")
def test_user_fixture(db_session: Session):
    unique_id = random.randint(1, 100000)
    password = "fixturepass"
    user_create = schemas.UserCreate(username=f"fixtureuser_{unique_id}", email=f"fixture_{unique_id}@example.com", password=password, role="engineer")
    user = crud.create_user(db_session, user=user_create, pwd_context=pwd_context)
    return user, password

@pytest.fixture(name="auth_token")
def auth_token_fixture(client: TestClient, test_user: tuple):
    user, password = test_user
    response = client.post(
        "/token",
        data={
            "username": user.username,
            "password": password
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(name="test_project_create")
def test_project_create_fixture():
    return schemas.ProjectCreate(title="Test Project", description="A project for testing.")

@pytest.fixture(name="test_project")
def test_project_fixture(client: TestClient, test_user: tuple, auth_token: str, test_project_create: schemas.ProjectCreate):
    user, _ = test_user
    response = client.post(
        f"/users/{user.id}/projects/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json=test_project_create.model_dump()
    )
    assert response.status_code == 200
    return response.json()


# --- Integration Tests ---

def test_create_user_api(client: TestClient, db_session: Session, test_user_create: schemas.UserCreate):
    response = client.post(
        "/users/",
        json=test_user_create.model_dump()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_create.username
    assert data["email"] == test_user_create.email
    assert "id" in data

def test_login_for_access_token(client: TestClient, test_user: tuple, test_user_create: schemas.UserCreate):
    user, password = test_user
    response = client.post(
        "/token",
        data={
            "username": user.username,
            "password": password
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_read_users_me(client: TestClient, auth_token: str, test_user: tuple):
    user, _ = test_user
    response = client.get(
        "/users/me/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user.username
    assert data["email"] == user.email

def test_create_project_api(client: TestClient, test_user: tuple, auth_token: str, test_project_create: schemas.ProjectCreate):
    user, _ = test_user
    response = client.post(
        f"/users/{user.id}/projects/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json=test_project_create.model_dump()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_project_create.title
    assert data["owner_id"] == user.id

def test_read_projects_api(client: TestClient, auth_token: str, test_project: dict):
    response = client.get(
        "/projects/",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == test_project["title"]

def test_update_project_api(client: TestClient, test_user: models.User, auth_token: str, test_project: dict):
    updated_title = "Updated Project via API"
    project_update = schemas.ProjectCreate(title=updated_title)
    response = client.put(
        f"/projects/{test_project['id']}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json=project_update.model_dump(exclude_unset=True)
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_title

def test_delete_project_api(client: TestClient, test_user: models.User, auth_token: str, test_project: dict):
    response = client.delete(
        f"/projects/{test_project['id']}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == 204
    response = client.get(
        f"/projects/{test_project['id']}",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    assert response.status_code == 404

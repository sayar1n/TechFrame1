import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.database import Base
from backend import models, schemas, crud
from passlib.context import CryptContext

# Setup for test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for testing
@pytest.fixture(name="db_session")
def db_session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="pwd_context")
def pwd_context_fixture():
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- User CRUD Tests ---
def test_create_user(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="testuser", email="test@example.com", password="shortpass")
    user = crud.create_user(db_session, user_in, pwd_context)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert crud.verify_password("shortpass", user.hashed_password, pwd_context)

def test_get_user(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="anotheruser", email="another@example.com", password="anothershort")
    created_user = crud.create_user(db_session, user_in, pwd_context)
    fetched_user = crud.get_user(db_session, created_user.id)
    assert fetched_user.username == "anotheruser"

def test_get_user_by_email(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="emailuser", email="email@example.com", password="emailshort")
    created_user = crud.create_user(db_session, user_in, pwd_context)
    fetched_user = crud.get_user_by_email(db_session, "email@example.com")
    assert fetched_user.username == "emailuser"

def test_get_user_by_username(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="usernameuser", email="username@example.com", password="usernameshort")
    created_user = crud.create_user(db_session, user_in, pwd_context)
    fetched_user = crud.get_user_by_username(db_session, "usernameuser")
    assert fetched_user.email == "username@example.com"

# --- Project CRUD Tests ---
def test_create_project(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="projectowner", email="owner@example.com", password="ownershort")
    owner = crud.create_user(db_session, user_in, pwd_context)
    project_in = schemas.ProjectCreate(title="Test Project", description="Description for test project")
    project = crud.create_user_project(db_session, project_in, owner.id)
    assert project.title == "Test Project"
    assert project.description == "Description for test project"
    assert project.owner_id == owner.id

def test_get_project(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="getteruser", email="getter@example.com", password="gettershort")
    owner = crud.create_user(db_session, user_in, pwd_context)
    project_in = schemas.ProjectCreate(title="Fetch Project", description="Description for fetch project")
    created_project = crud.create_user_project(db_session, project_in, owner.id)
    fetched_project = crud.get_project(db_session, created_project.id)
    assert fetched_project.title == "Fetch Project"

def test_update_project(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="updateruser", email="updater@example.com", password="updateshort")
    owner = crud.create_user(db_session, user_in, pwd_context)
    project_in = schemas.ProjectCreate(title="Old Title", description="Old Description")
    project = crud.create_user_project(db_session, project_in, owner.id)
    
    update_data = schemas.ProjectCreate(title="New Title", description="New Description")
    updated_project = crud.update_project(db_session, project.id, update_data)
    assert updated_project.title == "New Title"
    assert updated_project.description == "New Description"

def test_delete_project(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="deleteruser", email="deleter@example.com", password="deleteshort")
    owner = crud.create_user(db_session, user_in, pwd_context)
    project_in = schemas.ProjectCreate(title="Project to Delete", description="Temporary Project")
    project = crud.create_user_project(db_session, project_in, owner.id)
    
    crud.delete_project(db_session, project.id)
    deleted_project = crud.get_project(db_session, project.id)
    assert deleted_project is None

# --- Defect CRUD Tests ---
def test_create_defect(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="reporter", email="reporter@example.com", password="repshort")
    reporter = crud.create_user(db_session, user_in, pwd_context)
    project_in = schemas.ProjectCreate(title="Defect Project", description="Project for defects")
    project = crud.create_user_project(db_session, project_in, reporter.id)

    defect_in = schemas.DefectCreate(title="Bug 1", description="Critical bug found", project_id=project.id, priority=schemas.DefectPriority.critical)
    defect = crud.create_defect(db_session, defect_in, reporter.id)
    assert defect.title == "Bug 1"
    assert defect.reporter_id == reporter.id
    assert defect.project_id == project.id
    assert defect.priority == schemas.DefectPriority.critical

def test_get_defect(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="defectreader", email="reader@example.com", password="readshort")
    reporter = crud.create_user(db_session, user_in, pwd_context)
    project_in = schemas.ProjectCreate(title="Read Defect Project", description="Project for reading defects")
    project = crud.create_user_project(db_session, project_in, reporter.id)
    defect_in = schemas.DefectCreate(title="Read Bug", description="To be read", project_id=project.id)
    created_defect = crud.create_defect(db_session, defect_in, reporter.id)

    fetched_defect = crud.get_defect(db_session, created_defect.id)
    assert fetched_defect.title == "Read Bug"

def test_update_defect(db_session: Session, pwd_context: CryptContext):
    user_in_reporter = schemas.UserCreate(username="upd_reporter", email="upd_reporter@example.com", password="updrep")
    reporter = crud.create_user(db_session, user_in_reporter, pwd_context)
    user_in_assignee = schemas.UserCreate(username="upd_assignee", email="upd_assignee@example.com", password="updass")
    assignee = crud.create_user(db_session, user_in_assignee, pwd_context)

    project_in = schemas.ProjectCreate(title="Update Defect Project", description="Project for updating defects")
    project = crud.create_user_project(db_session, project_in, reporter.id)

    defect_in = schemas.DefectCreate(title="Old Bug Title", description="Old Bug Description", project_id=project.id, assignee_id=reporter.id)
    defect = crud.create_defect(db_session, defect_in, reporter.id)

    update_data = schemas.DefectUpdate(title="New Bug Title", status=schemas.DefectStatus.in_progress, assignee_id=assignee.id)
    updated_defect = crud.update_defect(db_session, defect.id, update_data)

    assert updated_defect.title == "New Bug Title"
    assert updated_defect.status == schemas.DefectStatus.in_progress
    assert updated_defect.assignee_id == assignee.id

def test_delete_defect(db_session: Session, pwd_context: CryptContext):
    user_in = schemas.UserCreate(username="del_reporter", email="del_reporter@example.com", password="delrep")
    reporter = crud.create_user(db_session, user_in, pwd_context)
    project_in = schemas.ProjectCreate(title="Delete Defect Project", description="Project for deleting defects")
    project = crud.create_user_project(db_session, project_in, reporter.id)
    defect_in = schemas.DefectCreate(title="Delete Bug", description="To be deleted", project_id=project.id)
    defect = crud.create_defect(db_session, defect_in, reporter.id)

    crud.delete_defect(db_session, defect.id)
    deleted_defect = crud.get_defect(db_session, defect.id)
    assert deleted_defect is None

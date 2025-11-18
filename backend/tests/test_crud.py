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

@pytest.fixture(name="test_user_create")
def test_user_create_fixture():
    return schemas.UserCreate(username="testuser", email="test@example.com", password="shortpass", role="engineer")

@pytest.fixture(name="test_user")
def test_user_fixture(db_session: Session, test_user_create: schemas.UserCreate):
    user = crud.create_user(db_session, user=test_user_create, pwd_context=pwd_context)
    return user

@pytest.fixture(name="test_project_create")
def test_project_create_fixture():
    return schemas.ProjectCreate(title="Test Project", description="A project for testing.")

@pytest.fixture(name="test_project")
def test_project_fixture(db_session: Session, test_user: models.User, test_project_create: schemas.ProjectCreate):
    project = crud.create_user_project(db_session, project=test_project_create, user_id=test_user.id)
    return project

@pytest.fixture(name="test_defect_create")
def test_defect_create_fixture(test_project: models.Project):
    return schemas.DefectCreate(title="Test Defect", description="A defect for testing.", project_id=test_project.id)

@pytest.fixture(name="test_defect")
def test_defect_fixture(db_session: Session, test_user: models.User, test_defect_create: schemas.DefectCreate):
    defect = crud.create_defect(db_session, defect=test_defect_create, reporter_id=test_user.id)
    return defect

@pytest.fixture(name="test_comment_create")
def test_comment_create_fixture(test_defect: models.Defect):
    return schemas.CommentCreate(content="Test comment content.", defect_id=test_defect.id)

@pytest.fixture(name="test_comment")
def test_comment_fixture(db_session: Session, test_user: models.User, test_comment_create: schemas.CommentCreate):
    comment = crud.create_comment(db_session, comment=test_comment_create, author_id=test_user.id)
    return comment

@pytest.fixture(name="test_attachment_create")
def test_attachment_create_fixture(test_defect: models.Defect):
    return schemas.AttachmentCreate(filename="test_file.txt", file_path="/path/to/test_file.txt", defect_id=test_defect.id)

@pytest.fixture(name="test_attachment")
def test_attachment_fixture(db_session: Session, test_user: models.User, test_attachment_create: schemas.AttachmentCreate):
    attachment = crud.create_attachment(db_session, attachment=test_attachment_create, uploader_id=test_user.id)
    return attachment


# --- Test Cases ---

def test_verify_password(db_session: Session):
    test_password = "securepassword"
    user_create = schemas.UserCreate(username="tempuser", email="temp@example.com", password=test_password, role="engineer")
    user = crud.create_user(db_session, user=user_create, pwd_context=pwd_context)

    assert crud.verify_password(test_password, user.hashed_password, pwd_context)
    assert not crud.verify_password("wrongpass", user.hashed_password, pwd_context)

def test_create_user(db_session: Session, test_user_create: schemas.UserCreate):
    user = crud.create_user(db_session, user=test_user_create, pwd_context=pwd_context)
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "engineer"
    assert user.is_active is True

def test_get_user(db_session: Session, test_user: models.User):
    user = crud.get_user(db_session, user_id=test_user.id)
    assert user.username == "testuser"

def test_get_user_by_email(db_session: Session, test_user: models.User):
    user = crud.get_user_by_email(db_session, email="test@example.com")
    assert user.username == "testuser"

def test_get_user_by_username(db_session: Session, test_user: models.User):
    user = crud.get_user_by_username(db_session, username="testuser")
    assert user.email == "test@example.com"

def test_create_project(db_session: Session, test_user: models.User, test_project_create: schemas.ProjectCreate):
    project = crud.create_user_project(db_session, project=test_project_create, user_id=test_user.id)
    assert project.id is not None
    assert project.title == "Test Project"
    assert project.owner_id == test_user.id

def test_get_project(db_session: Session, test_project: models.Project):
    project = crud.get_project(db_session, project_id=test_project.id)
    assert project.title == "Test Project"

def test_update_project(db_session: Session, test_project: models.Project):
    updated_title = "Updated Project Title"
    updated_description = "Updated project description."
    project_update = schemas.ProjectCreate(title=updated_title, description=updated_description)
    updated_project = crud.update_project(db_session, project_id=test_project.id, project=project_update)
    assert updated_project.title == updated_title
    assert updated_project.description == updated_description

def test_delete_project(db_session: Session, test_project: models.Project):
    crud.delete_project(db_session, project_id=test_project.id)
    deleted_project = crud.get_project(db_session, project_id=test_project.id)
    assert deleted_project is None

def test_create_defect(db_session: Session, test_user: models.User, test_defect_create: schemas.DefectCreate):
    defect = crud.create_defect(db_session, defect=test_defect_create, reporter_id=test_user.id)
    assert defect.id is not None
    assert defect.title == "Test Defect"
    assert defect.reporter_id == test_user.id
    assert defect.project_id == test_defect_create.project_id

def test_get_defect(db_session: Session, test_defect: models.Defect):
    defect = crud.get_defect(db_session, defect_id=test_defect.id)
    assert defect.title == "Test Defect"

def test_update_defect(db_session: Session, test_defect: models.Defect):
    updated_title = "Updated Defect Title"
    updated_status = schemas.DefectStatus.closed
    defect_update = schemas.DefectUpdate(title=updated_title, status=updated_status)
    updated_defect = crud.update_defect(db_session, defect_id=test_defect.id, defect=defect_update)
    assert updated_defect.title == updated_title
    assert updated_defect.status == updated_status

def test_delete_defect(db_session: Session, test_defect: models.Defect):
    crud.delete_defect(db_session, defect_id=test_defect.id)
    deleted_defect = crud.get_defect(db_session, defect_id=test_defect.id)
    assert deleted_defect is None

def test_create_comment(db_session: Session, test_user: models.User, test_comment_create: schemas.CommentCreate):
    comment = crud.create_comment(db_session, comment=test_comment_create, author_id=test_user.id)
    assert comment.id is not None
    assert comment.content == "Test comment content."
    assert comment.author_id == test_user.id
    assert comment.defect_id == test_comment_create.defect_id

def test_get_comment(db_session: Session, test_comment: models.Comment):
    comment = crud.get_comment(db_session, comment_id=test_comment.id)
    assert comment.content == "Test comment content."

def test_update_comment(db_session: Session, test_comment: models.Comment):
    updated_content = "Updated comment content."
    comment_update = schemas.CommentCreate(content=updated_content, defect_id=test_comment.defect_id)
    updated_comment = crud.update_comment(db_session, comment_id=test_comment.id, comment=comment_update)
    assert updated_comment.content == updated_content

def test_delete_comment(db_session: Session, test_comment: models.Comment):
    crud.delete_comment(db_session, comment_id=test_comment.id)
    deleted_comment = crud.get_comment(db_session, comment_id=test_comment.id)
    assert deleted_comment is None

def test_create_attachment(db_session: Session, test_user: models.User, test_attachment_create: schemas.AttachmentCreate):
    attachment = crud.create_attachment(db_session, attachment=test_attachment_create, uploader_id=test_user.id)
    assert attachment.id is not None
    assert attachment.filename == "test_file.txt"
    assert attachment.file_path == "/path/to/test_file.txt"
    assert attachment.uploader_id == test_user.id
    assert attachment.defect_id == test_attachment_create.defect_id

def test_get_attachment(db_session: Session, test_attachment: models.Attachment):
    attachment = crud.get_attachment(db_session, attachment_id=test_attachment.id)
    assert attachment.filename == "test_file.txt"

def test_update_attachment(db_session: Session, test_attachment: models.Attachment):
    updated_filename = "updated_file.pdf"
    attachment_update = schemas.AttachmentCreate(filename=updated_filename, file_path="/new/path.pdf", defect_id=test_attachment.defect_id)
    updated_attachment = crud.update_attachment(db_session, attachment_id=test_attachment.id, attachment=attachment_update)
    assert updated_attachment.filename == updated_filename
    assert updated_attachment.file_path == "/new/path.pdf"

def test_delete_attachment(db_session: Session, test_attachment: models.Attachment):
    crud.delete_attachment(db_session, attachment_id=test_attachment.id)
    deleted_attachment = crud.get_attachment(db_session, attachment_id=test_attachment.id)
    assert deleted_attachment is None

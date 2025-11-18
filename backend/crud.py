from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password, pwd_context):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password, pwd_context):
    return pwd_context.hash(password.encode('utf-8')[:72]) # Кодируем пароль в байты и усекаем до 72 байт

# --- User CRUD operations ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, pwd_context: CryptContext):
    hashed_password = get_password_hash(user.password, pwd_context)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_role(db: Session, user_id: int, new_role: schemas.UserRole):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.role = new_role
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

# --- Project CRUD operations ---
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()

def create_user_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(**project.model_dump(), owner_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, project: schemas.ProjectCreate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        update_data = project.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

# --- Defect CRUD operations ---
def get_defect(db: Session, defect_id: int):
    return db.query(models.Defect).filter(models.Defect.id == defect_id).first()

def get_defects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    status: Optional[schemas.DefectStatus] = None,
    priority: Optional[schemas.DefectPriority] = None,
    assignee_id: Optional[int] = None,
    reporter_id: Optional[int] = None,
    created_start_date: Optional[datetime] = None,
    created_end_date: Optional[datetime] = None,
    due_start_date: Optional[datetime] = None,
    due_end_date: Optional[datetime] = None,
    search_query: Optional[str] = None,
):
    query = db.query(models.Defect)
    if project_id:
        query = query.filter(models.Defect.project_id == project_id)
    if status:
        query = query.filter(models.Defect.status == status)
    if priority:
        query = query.filter(models.Defect.priority == priority)
    if assignee_id:
        query = query.filter(models.Defect.assignee_id == assignee_id)
    if reporter_id:
        query = query.filter(models.Defect.reporter_id == reporter_id)
    if created_start_date:
        query = query.filter(models.Defect.created_at >= created_start_date)
    if created_end_date:
        query = query.filter(models.Defect.created_at <= created_end_date)
    if due_start_date:
        query = query.filter(models.Defect.due_date >= due_start_date)
    if due_end_date:
        query = query.filter(models.Defect.due_date <= due_end_date)
    if search_query:
        query = query.filter(
            (models.Defect.title.contains(search_query)) |
            (models.Defect.description.contains(search_query))
        )
    return query.offset(skip).limit(limit).all()

def create_defect(db: Session, defect: schemas.DefectCreate, reporter_id: int):
    db_defect = models.Defect(**defect.model_dump(exclude_unset=True), reporter_id=reporter_id)
    db.add(db_defect)
    db.commit()
    db.refresh(db_defect)
    return db_defect

def update_defect(db: Session, defect_id: int, defect: schemas.DefectUpdate):
    db_defect = db.query(models.Defect).filter(models.Defect.id == defect_id).first()
    if db_defect:
        update_data = defect.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_defect, key, value)
        db.add(db_defect)
        db.commit()
        db.refresh(db_defect)
    return db_defect

def delete_defect(db: Session, defect_id: int):
    db_defect = db.query(models.Defect).filter(models.Defect.id == defect_id).first()
    if db_defect:
        db.delete(db_defect)
        db.commit()
    return db_defect

# --- Comment CRUD operations ---
def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def create_comment(db: Session, comment: schemas.CommentCreate, author_id: int):
    db_comment = models.Comment(**comment.model_dump(), author_id=author_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: int, comment: schemas.CommentCreate):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        update_data = comment.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_comment, key, value)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment

# --- Attachment CRUD operations ---
def get_attachment(db: Session, attachment_id: int):
    return db.query(models.Attachment).filter(models.Attachment.id == attachment_id).first()

def create_attachment(db: Session, attachment: schemas.AttachmentCreate, uploader_id: int, filename: str, file_path: str):
    db_attachment = models.Attachment(
        defect_id=attachment.defect_id,
        uploader_id=uploader_id,
        filename=filename,
        file_path=file_path
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def update_attachment(db: Session, attachment_id: int, attachment: schemas.AttachmentCreate):
    db_attachment = db.query(models.Attachment).filter(models.Attachment.id == attachment_id).first()
    if db_attachment:
        update_data = attachment.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_attachment, key, value)
        db.add(db_attachment)
        db.commit()
        db.refresh(db_attachment)
    return db_attachment

def delete_attachment(db: Session, attachment_id: int):
    db_attachment = db.query(models.Attachment).filter(models.Attachment.id == attachment_id).first()
    if db_attachment:
        db.delete(db_attachment)
        db.commit()
    return db_attachment

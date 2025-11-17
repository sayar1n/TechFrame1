from datetime import datetime
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserRole(str, Enum):
    manager = "manager"
    engineer = "engineer"
    observer = "observer"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.engineer

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    owner_id: int
    defects: List["Defect"] = [] # Forward reference

    model_config = ConfigDict(from_attributes=True)

class DefectPriority(str, Enum):
    low = "Низкий"
    medium = "Средний"
    high = "Высокий"
    critical = "Критический"

class DefectStatus(str, Enum):
    new = "Новая"
    in_progress = "В работе"
    on_review = "На проверке"
    closed = "Закрыта"
    cancelled = "Отменена"

class DefectBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: DefectPriority = DefectPriority.low
    status: DefectStatus = DefectStatus.new
    due_date: Optional[datetime] = None

class DefectCreate(DefectBase):
    project_id: int
    assignee_id: Optional[int] = None

class DefectUpdate(DefectBase):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[DefectPriority] = None
    status: Optional[DefectStatus] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

class Defect(DefectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    reporter_id: int
    project_id: int
    comments: List["Comment"] = [] # Forward reference
    attachments: List["Attachment"] = [] # Forward reference

    model_config = ConfigDict(from_attributes=True)

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    defect_id: int

class Comment(CommentBase):
    id: int
    created_at: datetime
    author_id: int
    defect_id: int

    model_config = ConfigDict(from_attributes=True)

class AttachmentBase(BaseModel):
    filename: str
    file_path: str

class AttachmentCreate(AttachmentBase):
    defect_id: int

class Attachment(AttachmentBase):
    id: int
    uploaded_at: datetime
    uploader_id: int
    defect_id: int

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Update forward refs
Project.model_rebuild()
Defect.model_rebuild()

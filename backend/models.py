from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum("manager", "engineer", "observer", "admin", name="user_roles"), default="engineer", nullable=False)
    is_active = Column(Boolean, default=True)

    projects = relationship("Project", back_populates="owner")
    defects_reported = relationship("Defect", foreign_keys="[Defect.reporter_id]", back_populates="reporter")
    defects_assigned = relationship("Defect", foreign_keys="[Defect.assignee_id]", back_populates="assignee")
    comments = relationship("Comment", back_populates="author")
    attachments = relationship("Attachment", back_populates="uploader")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="projects")
    defects = relationship("Defect", back_populates="project")

class Defect(Base):
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum("Низкий", "Средний", "Высокий", "Критический", name="defect_priorities"), default="Низкий", nullable=False)
    status = Column(Enum("Новая", "В работе", "На проверке", "Закрыта", "Отменена", name="defect_statuses"), default="Новая", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    reporter = relationship("User", foreign_keys="[Defect.reporter_id]", back_populates="defects_reported")
    assignee = relationship("User", foreign_keys="[Defect.assignee_id]", back_populates="defects_assigned")
    project = relationship("Project", back_populates="defects")
    comments = relationship("Comment", back_populates="defect")
    attachments = relationship("Attachment", back_populates="defect")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    defect_id = Column(Integer, ForeignKey("defects.id"), nullable=False)

    author = relationship("User", back_populates="comments")
    defect = relationship("Defect", back_populates="comments")

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    defect_id = Column(Integer, ForeignKey("defects.id"), nullable=False)

    uploader = relationship("User", back_populates="attachments")
    defect = relationship("Defect", back_populates="attachments")

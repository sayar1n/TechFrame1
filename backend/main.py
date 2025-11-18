from datetime import datetime, timedelta
from typing import Optional, List
import csv
from io import StringIO
import logging
import time
import io
import shutil
import os

from fastapi import FastAPI, Depends, HTTPException, status, Query, Request, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from openpyxl import Workbook
from starlette.responses import FileResponse

from backend import crud, models, schemas
from .database import engine, SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # Next.js frontend default port
    "http://localhost:8000", # FastAPI backend default port
    # Add other origins as needed in production
]

# Объединяем предопределенные origins с вашим локальным IP-адресом
alle_origins = origins + ["http://10.0.85.2:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=alle_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer for JWT token
# to get a string like this run: openssl rand -hex 32
SECRET_KEY = "your-secret-key" # TODO: Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"Attempting to decode token: {token}") # Добавлено логирование
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}") # Добавлено логирование
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# --- API Endpoints ---

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Defect Management API"}

# Authentication endpoints
@app.post("/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password, pwd_context):
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"User {user.username} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.post("/register/", response_model=schemas.User, tags=["Users"])
async def register_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user_username = crud.get_user_by_username(db, username=user.username)
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    user.role = schemas.UserRole.observer  # Принудительно устанавливаем роль "observer"
    return crud.create_user(db=db, user=user, pwd_context=pwd_context)

@app.get("/users/me/", response_model=schemas.User, tags=["Users"])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    logger.info(f"User {current_user.username} accessed their own profile.")
    return current_user

@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}/role", response_model=schemas.User, tags=["Users"])
async def update_user_role(
    user_id: int, 
    new_role: schemas.UserRole, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    if current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]:
        raise HTTPException(status_code=403, detail="Not authorized to change user roles")
    
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = crud.update_user_role(db, user_id, new_role)
    return updated_user

@app.get("/admin/users/", response_model=List[schemas.User], tags=["Admin"])
async def read_all_users_admin(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    if current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access admin features")
    users = crud.get_users(db)
    return users

@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        logger.warning(f"User {current_user.username} tried to access non-existent user with ID: {user_id}.")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User {current_user.username} accessed user with ID: {user_id}.")
    return db_user

# Project API endpoints
@app.post("/users/{user_id}/projects/", response_model=schemas.Project, tags=["Projects"])
def create_project_for_user(
    user_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)
):
    if current_user.id != user_id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]:
        logger.warning(f"User {current_user.username} tried to create project for another user {user_id}.")
        raise HTTPException(status_code=403, detail="Not authorized to create projects for this user")
    new_project = crud.create_user_project(db=db, project=project, user_id=user_id)
    logger.info(f"User {current_user.username} created project {new_project.title} (ID: {new_project.id}).")
    return new_project

@app.get("/projects/", response_model=List[schemas.Project], tags=["Projects"])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    logger.info(f"User {current_user.username} accessed list of projects.")
    return projects

@app.get("/projects/{project_id}", response_model=schemas.Project, tags=["Projects"])
def read_project(project_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        logger.warning(f"User {current_user.username} tried to access non-existent project with ID: {project_id}.")
        raise HTTPException(status_code=404, detail="Project not found")
    logger.info(f"User {current_user.username} accessed project {db_project.title} (ID: {project_id}).")
    return db_project

@app.put("/projects/{project_id}", response_model=schemas.Project, tags=["Projects"])
def update_project(
    project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)
):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        logger.warning(f"User {current_user.username} tried to update non-existent project with ID: {project_id}.")
        raise HTTPException(status_code=404, detail="Project not found")
    if db_project.owner_id != current_user.id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]: # Only owner or manager/admin can update
        logger.warning(f"User {current_user.username} not authorized to update project {project_id}.")
        raise HTTPException(status_code=403, detail="Not authorized to update this project")
    updated_project = crud.update_project(db=db, project_id=project_id, project=project)
    logger.info(f"User {current_user.username} updated project {updated_project.title} (ID: {project_id}).")
    return updated_project

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Projects"])
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        logger.warning(f"User {current_user.username} tried to delete non-existent project with ID: {project_id}.")
        raise HTTPException(status_code=404, detail="Project not found")
    if db_project.owner_id != current_user.id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]: # Only owner or manager/admin can delete
        logger.warning(f"User {current_user.username} not authorized to delete project {project_id}.")
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    crud.delete_project(db=db, project_id=project_id)
    logger.info(f"User {current_user.username} deleted project (ID: {project_id}).")
    return

# Defect API endpoints
@app.post("/projects/{project_id}/defects/", response_model=schemas.Defect, tags=["Defects"])
def create_defect_for_project(
    project_id: int, defect: schemas.DefectCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)
):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    # Only members of the project or managers can create defects
    if current_user.id != db_project.owner_id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.engineer, schemas.UserRole.admin]:
        raise HTTPException(status_code=403, detail="Not authorized to create defects for this project")
    new_defect = crud.create_defect(db=db, defect=defect, reporter_id=current_user.id)
    return new_defect

@app.post("/defects/", response_model=schemas.Defect, tags=["Defects"])
async def create_defect_global(
    defect: schemas.DefectCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    if current_user.role not in [schemas.UserRole.manager, schemas.UserRole.engineer, schemas.UserRole.admin]:
        raise HTTPException(status_code=403, detail="Not authorized to create defects")
    return crud.create_defect(db=db, defect=defect, reporter_id=current_user.id)

@app.get("/defects/", response_model=List[schemas.Defect], tags=["Defects"])
def read_defects(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = Query(None),
    status: Optional[schemas.DefectStatus] = Query(None),
    priority: Optional[schemas.DefectPriority] = Query(None),
    assignee_id: Optional[int] = Query(None),
    reporter_id: Optional[int] = Query(None),
    created_start_date: Optional[datetime] = Query(None),
    created_end_date: Optional[datetime] = Query(None),
    due_start_date: Optional[datetime] = Query(None),
    due_end_date: Optional[datetime] = Query(None),
    search_query: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    defects = crud.get_defects(
        db=db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        reporter_id=reporter_id,
        created_start_date=created_start_date,
        created_end_date=created_end_date,
        due_start_date=due_start_date,
        due_end_date=due_end_date,
        search_query=search_query,
    )
    logger.info(f"User {current_user.username} accessed list of defects with filters.")
    return defects

@app.get("/defects/{defect_id}", response_model=schemas.Defect, tags=["Defects"])
def read_defect(defect_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_defect = crud.get_defect(db, defect_id=defect_id)
    if db_defect is None:
        logger.warning(f"User {current_user.username} tried to access non-existent defect with ID: {defect_id}.")
        raise HTTPException(status_code=404, detail="Defect not found")
    logger.info(f"User {current_user.username} accessed defect {db_defect.title} (ID: {defect_id}).")
    return db_defect

@app.put("/defects/{defect_id}", response_model=schemas.Defect, tags=["Defects"])
def update_defect(
    defect_id: int, defect: schemas.DefectUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)
):
    db_defect = crud.get_defect(db, defect_id=defect_id)
    if db_defect is None:
        logger.warning(f"User {current_user.username} tried to update non-existent defect with ID: {defect_id}.")
        raise HTTPException(status_code=404, detail="Defect not found")
    # Only reporter, assignee, or manager can update
    if current_user.id not in [db_defect.reporter_id, db_defect.assignee_id] and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]:
        logger.warning(f"User {current_user.username} not authorized to update defect {defect_id}.")
        raise HTTPException(status_code=403, detail="Not authorized to update this defect")
    updated_defect = crud.update_defect(db=db, defect_id=defect_id, defect=defect)
    logger.info(f"User {current_user.username} updated defect {updated_defect.title} (ID: {defect_id}).")
    return updated_defect

@app.delete("/defects/{defect_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Defects"])
def delete_defect(defect_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_defect = crud.get_defect(db, defect_id=defect_id)
    if db_defect is None:
        logger.warning(f"User {current_user.username} tried to delete non-existent defect with ID: {defect_id}.")
        raise HTTPException(status_code=404, detail="Defect not found")
    # Only reporter or manager can delete
    if current_user.id != db_defect.reporter_id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]:
        logger.warning(f"User {current_user.username} not authorized to delete defect {defect_id}.")
        raise HTTPException(status_code=403, detail="Not authorized to delete this defect")
    crud.delete_defect(db=db, defect_id=defect_id)
    logger.info(f"User {current_user.username} deleted defect (ID: {defect_id}).")
    return

# Comment API endpoints
@app.post("/defects/{defect_id}/comments/", response_model=schemas.Comment, tags=["Comments"])
def create_comment_for_defect(
    defect_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)
):
    db_defect = crud.get_defect(db, defect_id=defect_id)
    if db_defect is None:
        logger.warning(f"User {current_user.username} tried to create comment for non-existent defect with ID: {defect_id}.")
        raise HTTPException(status_code=404, detail="Defect not found")
    new_comment = crud.create_comment(db=db, comment=comment, author_id=current_user.id)
    logger.info(f"User {current_user.username} added comment (ID: {new_comment.id}) to defect {defect_id}.")
    return new_comment

@app.get("/defects/{defect_id}/comments/", response_model=List[schemas.Comment], tags=["Comments"])
def read_comments_for_defect(defect_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    # Add authorization check if needed, for now all authenticated users can view comments
    comments = db.query(models.Comment).filter(models.Comment.defect_id == defect_id).offset(skip).limit(limit).all()
    logger.info(f"User {current_user.username} accessed comments for defect {defect_id}.")
    return comments

@app.put("/comments/{comment_id}", response_model=schemas.Comment, tags=["Comments"])
def update_comment(
    comment_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)
):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        logger.warning(f"User {current_user.username} tried to update non-existent comment with ID: {comment_id}.")
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_id != current_user.id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]: # Only author or manager/admin can update
        logger.warning(f"User {current_user.username} not authorized to update comment {comment_id}.")
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    updated_comment = crud.update_comment(db=db, comment_id=comment_id, comment=comment)
    logger.info(f"User {current_user.username} updated comment (ID: {comment_id}) for defect {updated_comment.defect_id}.")
    return updated_comment

@app.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comments"])
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        logger.warning(f"User {current_user.username} tried to delete non-existent comment with ID: {comment_id}.")
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.author_id != current_user.id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]: # Only author or manager/admin can delete
        logger.warning(f"User {current_user.username} not authorized to delete comment {comment_id}.")
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    crud.delete_comment(db=db, comment_id=comment_id)
    logger.info(f"User {current_user.username} deleted comment (ID: {comment_id}).")
    return

# Attachment API endpoints
@app.post("/defects/{defect_id}/attachments/", response_model=schemas.Attachment, tags=["Attachments"])
def create_upload_attachment_for_defect(
    defect_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_defect = crud.get_defect(db, defect_id=defect_id)
    if db_defect is None:
        logger.warning(f"User {current_user.username} tried to create attachment for non-existent defect with ID: {defect_id}.")
        raise HTTPException(status_code=404, detail="Defect not found")
    
    # Check if the user is authorized to add attachments to this defect
    if current_user.role not in [schemas.UserRole.manager, schemas.UserRole.engineer, schemas.UserRole.admin]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to add attachments")

    upload_dir = f"./attachments/{defect_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_location = f"{upload_dir}/{file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    attachment_create = schemas.AttachmentCreate(defect_id=defect_id)
    new_attachment = crud.create_attachment(db=db, attachment=attachment_create, uploader_id=current_user.id, filename=file.filename, file_path=file_location)
    logger.info(f"User {current_user.username} added attachment {new_attachment.filename} (ID: {new_attachment.id}) to defect {defect_id}.")
    return new_attachment

@app.get("/defects/{defect_id}/attachments/", response_model=List[schemas.Attachment], tags=["Attachments"])
def read_attachments_for_defect(defect_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    # Add authorization check if needed, for now all authenticated users can view attachments
    attachments = db.query(models.Attachment).filter(models.Attachment.defect_id == defect_id).offset(skip).limit(limit).all()
    logger.info(f"User {current_user.username} accessed attachments for defect {defect_id}.")
    return attachments

@app.get("/defects/{defect_id}/attachments/{attachment_id}/download", tags=["Attachments"], summary="Download an attachment")
def download_attachment(
    defect_id: int,
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_attachment = crud.get_attachment(db, attachment_id=attachment_id)
    if db_attachment is None or db_attachment.defect_id != defect_id:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    # Add authorization check if needed

    file_path = db_attachment.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(file_path, filename=db_attachment.filename)

@app.delete("/defects/{defect_id}/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Attachments"])
def delete_attachment(
    defect_id: int,
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_attachment = crud.get_attachment(db, attachment_id=attachment_id)
    if db_attachment is None or db_attachment.defect_id != defect_id:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    if current_user.id != db_attachment.uploader_id and current_user.role not in [schemas.UserRole.manager, schemas.UserRole.admin]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this attachment")

    file_path = db_attachment.file_path
    if os.path.exists(file_path):
        os.remove(file_path)

    crud.delete_attachment(db=db, attachment_id=attachment_id)
    logger.info(f"User {current_user.username} deleted attachment {db_attachment.filename} (ID: {attachment_id}) from defect {defect_id}.")
    return

# Reporting API endpoint
@app.get("/reports/defects/export", response_class=StreamingResponse, tags=["Reports"], summary="Export defects to CSV/Excel")
def export_defects_to_csv_excel(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
    format: str = Query("csv", pattern="^(csv|xlsx)$"),
    project_id: Optional[int] = Query(None),
    status: Optional[schemas.DefectStatus] = Query(None),
    priority: Optional[schemas.DefectPriority] = Query(None),
    assignee_id: Optional[int] = Query(None),
    reporter_id: Optional[int] = Query(None),
    created_start_date: Optional[datetime] = Query(None),
    created_end_date: Optional[datetime] = Query(None),
    due_start_date: Optional[datetime] = Query(None),
    due_end_date: Optional[datetime] = Query(None),
    search_query: Optional[str] = Query(None)
):
    if current_user.role not in [schemas.UserRole.manager, schemas.UserRole.observer, schemas.UserRole.admin]:
        logger.warning(f"User {current_user.username} not authorized to export reports.")
        raise HTTPException(status_code=403, detail="Not authorized to export reports")

    defects = crud.get_defects(
        db=db,
        project_id=project_id,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        reporter_id=reporter_id,
        created_start_date=created_start_date,
        created_end_date=created_end_date,
        due_start_date=due_start_date,
        due_end_date=due_end_date,
        search_query=search_query,
    )

    headers = {"Content-Disposition": f"attachment; filename=\"defects_report.{format}\""}

    if format == "csv":
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(["ID", "Title", "Description", "Priority", "Status", "Created At", "Updated At", "Due Date", "Reporter ID", "Assignee ID", "Project ID"])

        # Write data
        for defect in defects:
            writer.writerow([
                defect.id,
                defect.title,
                defect.description,
                defect.priority.value if defect.priority else "",
                defect.status.value if defect.status else "",
                defect.created_at.isoformat() if defect.created_at else "",
                defect.updated_at.isoformat() if defect.updated_at else "",
                defect.due_date.isoformat() if defect.due_date else "",
                defect.reporter_id,
                defect.assignee_id,
                defect.project_id
            ])

        output.seek(0)
        logger.info(f"User {current_user.username} exported defects report to CSV.")
        return StreamingResponse(output, headers=headers, media_type="text/csv")

    elif format == "xlsx":
        wb = Workbook()
        ws = wb.active
        ws.title = "Defects Report"

        # Write header
        ws.append(["ID", "Title", "Description", "Priority", "Status", "Created At", "Updated At", "Due Date", "Reporter ID", "Assignee ID", "Project ID"])

        # Write data
        for defect in defects:
            ws.append([
                defect.id,
                defect.title,
                defect.description,
                defect.priority.value if defect.priority else "",
                defect.status.value if defect.status else "",
                defect.created_at.isoformat() if defect.created_at else "",
                defect.updated_at.isoformat() if defect.updated_at else "",
                defect.due_date.isoformat() if defect.due_date else "",
                defect.reporter_id,
                defect.assignee_id,
                defect.project_id
            ])

        excel_file = io.BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)
        
        logger.info(f"User {current_user.username} exported defects report to XLSX.")
        return StreamingResponse(excel_file, headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    else:
        raise HTTPException(status_code=400, detail="Invalid format. Choose 'csv' or 'xlsx'.")

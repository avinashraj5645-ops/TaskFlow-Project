import time
import uuid
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, Base
import models
import schemas
from dependencies import get_db
from algorithms import insertion_sort

# Auth functions import karein
from auth import get_current_user, hash_password, create_access_token, verify_password
from dotenv import load_dotenv
load_dotenv()  # Server start hote hi .env load karega

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API with Hand-Rolled Engines")

PRIORITY_RANK = {"low": 1, "medium": 2, "high": 3}

# Logger Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Custom Logger Middleware CORS ke baad aayega
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    print(f"[{request.method}] Path: {request.url.path} - Completed in {process_time:.2f}ms | Status: {response.status_code}")
    response.headers["X-Process-Time-Ms"] = str(process_time)
    return response

@app.get("/")
def home():
    return {"message": "SQLite DB is active!"}

def parse_quick_add_description(description: str):
    title = description
    priority = "medium"
    due_date = None

    desc_lower = description.lower()
    if "urgent" in desc_lower or "high" in desc_lower:
        priority = "high"
    elif "low" in desc_lower:
        priority = "low"

    return title, priority, due_date


# ==========================================
# AUTH & USER ENDPOINTS (MISSING FIXED)
# ==========================================

@app.post("/users", status_code=status.HTTP_201_CREATED)
def signup(data: dict, db: Session = Depends(get_db)):
    try:
        email = data.get("email")
        password = data.get("password")
        name = data.get("name") or data.get("full_name")

        if not email or not password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        # 1. Existing user check
        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already registered")

        # 2. Hash password
        hashed_pwd = hash_password(password)

        # 3. Dynamic Column Detection (Prevent TypeError in models.User)
        user_kwargs = {"name": name, "email": email}
        if hasattr(models.User, "hashed_password"):
            user_kwargs["hashed_password"] = hashed_pwd
        elif hasattr(models.User, "password_hash"):
            user_kwargs["password_hash"] = hashed_pwd
        elif hasattr(models.User, "password"):
            user_kwargs["password"] = hashed_pwd

        # 4. Save to Database
        new_user = models.User(**user_kwargs)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"id": new_user.id, "name": new_user.name, "email": new_user.email}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        db.rollback()
        print(f"[/users ERROR]: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database or Server Error: {str(e)}"
        )


@app.post("/auth/login")
def login(credentials: dict, db: Session = Depends(get_db)):
    email = credentials.get("email")
    password = credentials.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email and password are required"
        )

    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token": access_token,  # Backward compatibility
        "token_type": "bearer",
        "user": {"id": user.id, "name": user.name, "email": user.email}
    }


@app.get("/users/me")
def get_user_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


@app.put("/users/me")
def update_user_profile(
    data: dict, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    if "name" in data:
        current_user.name = data["name"]
    if "email" in data:
        # Check if email is being changed and if it already exists
        if data["email"] != current_user.email:
            existing = db.query(models.User).filter(models.User.email == data["email"]).first()
            if existing:
                raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = data["email"]

    db.commit()
    db.refresh(current_user)
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


# ==========================================
# PROJECTS ENDPOINTS
# ==========================================

@app.post("/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(data: dict, db: Session = Depends(get_db)):
    project_name = data.get("name") or data.get("title")

    if not project_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Project name is required"
        )

    try:
        new_project = models.Project(
            id=str(uuid.uuid4()),
            name=project_name,
            owner_id=data.get("owner_id")
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Insertion Error: {str(e)}"
        )


@app.get("/projects", response_model=list[schemas.ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


@app.get("/projects/stats")
def get_project_stats(db: Session = Depends(get_db)):
    total_projects = db.query(models.Project).count()
    total_tasks = db.query(models.Task).count()
    completed_tasks = db.query(models.Task).filter(models.Task.completed == True).count()
    
    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks
    }


# ==========================================
# TASKS ENDPOINTS
# ==========================================

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    if task_data.project_id:
        project = db.query(models.Project).filter(models.Project.id == str(task_data.project_id)).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Project ID '{task_data.project_id}' does not exist"
            )

    try:
        task_dict = task_data.model_dump()
        task_dict["id"] = str(uuid.uuid4())
        
        new_task = models.Task(**task_dict)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task in DB: {str(e)}"
        )


@app.post("/tasks/quick-add", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def quick_add_task(payload: schemas.QuickAddRequest, db: Session = Depends(get_db)):
    if payload.project_id:
        project = db.query(models.Project).filter(models.Project.id == str(payload.project_id)).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail=f"Project with ID '{payload.project_id}' does not exist"
            )

    title, priority, due_date_hint = parse_quick_add_description(payload.description)

    try:
        db_task = models.Task(
            id=str(uuid.uuid4()),
            title=title,
            priority=priority,
            due_date=due_date_hint,
            project_id=payload.project_id,
            completed=False
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quick add failed: {str(e)}"
        )


@app.get("/tasks", response_model=list[schemas.TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(
    search: Optional[str] = None, 
    sort: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    db_tasks = db.query(models.Task).all()
    
    tasks_list = [
        {
            "id": str(t.id),
            "title": t.title,
            "due_date": t.due_date,
            "priority": t.priority,
            "completed": t.completed,
            "project_id": str(t.project_id) if t.project_id else None
        }
        for t in db_tasks
    ]

    if search:
        tasks_list = [t for t in tasks_list if search.lower() in t["title"].lower()]

    if sort == "priority":
        for t in tasks_list:
            t["_rank"] = PRIORITY_RANK.get(t["priority"], 1)
        insertion_sort(tasks_list, "_rank")
        for t in tasks_list:
            t.pop("_rank", None)
    elif sort in ["due", "due_date"]:
        for t in tasks_list:
            t["_due_key"] = t["due_date"] or "ZZZZ"
        insertion_sort(tasks_list, "_due_key")
        for t in tasks_list:
            t.pop("_due_key", None)

    return tasks_list


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task_status(task_id: str, payload: dict, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if "completed" in payload:
        task.completed = payload["completed"]
    if "title" in payload:
        task.title = payload["title"]

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None

class PasswordChangeSchema(BaseModel):
    current_password: str
    new_password: str

@app.put("/users/password")
def change_password(
    data: PasswordChangeSchema, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # 1. Purana password verify karein
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect current password"
        )

    # 2. Naya password hash karke save karein
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}
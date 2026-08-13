from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List

# --- User Schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


# --- Project Schemas ---
class ProjectCreate(BaseModel):
    name: str
    owner_id: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    owner_id: Optional[str] = None

    class Config:
        from_attributes = True


# --- Task Schemas ---
class TaskCreate(BaseModel):
    title: str
    due_date: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    # FIX: project_id ko Optional[str] kiya hai taaki UUID String easily accept ho sake
    project_id: Optional[str] = None 

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Task title cannot be empty or blank whitespace.")
        return trimmed

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    completed: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            trimmed = v.strip()
            if not trimmed:
                raise ValueError("Task title cannot be empty or blank whitespace.")
            return trimmed
        return v

class TaskResponse(BaseModel):
    id: str
    title: str
    priority: str
    completed: bool = False
    due_date: Optional[str] = None
    project_id: Optional[str] = None

    class Config:
        from_attributes = True


# --- Aggregation Stats Schema ---
class ProjectStatsResponse(BaseModel):
    project_id: str
    project_name: str
    total_tasks: int
    completed_tasks: int
    pending_tasks: int

class QuickAddRequest(BaseModel):
    description: str
    project_id: Optional[str] = None
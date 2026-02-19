from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid
from .user import User, UserRead


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field()  # String to match database schema
    


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    user_id: str  # String to match database schema


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskPatch(SQLModel):
    is_completed: Optional[bool] = None
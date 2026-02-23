from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
# Import using importlib to avoid duplicate registration issues
import importlib
import sys

# Check if models are already in sys.modules to prevent re-importing
if 'backend.src.models.task' not in sys.modules:
    task_module = importlib.import_module('.models.task', package='backend.src')
    Task = task_module.Task
    TaskCreate = task_module.TaskCreate
    TaskRead = task_module.TaskRead
    TaskUpdate = task_module.TaskUpdate
    TaskPatch = task_module.TaskPatch
else:
    task_module = sys.modules['backend.src.models.task']
    Task = task_module.Task
    TaskCreate = task_module.TaskCreate
    TaskRead = task_module.TaskRead
    TaskUpdate = task_module.TaskUpdate
    TaskPatch = task_module.TaskPatch

from ..services.task_service import (
    create_task, get_tasks, get_task, update_task,
    delete_task, toggle_task_completion
)
from ..database import get_session
from ..middleware.auth import get_current_user

# Import User model
if 'backend.src.models.user' not in sys.modules:
    user_module = importlib.import_module('.models.user', package='backend.src')
    User = user_module.User
else:
    user_module = sys.modules['backend.src.models.user']
    User = user_module.User


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskRead])
def read_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user"""
    tasks = get_tasks(session, current_user.id)
    return tasks


@router.post("/", response_model=TaskRead)
def create_task_for_user(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    db_task = create_task(session, task, current_user.id)
    return db_task


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific task for the current user"""
    task = get_task(session, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task_for_user(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific task for the current user"""
    updated_task = update_task(session, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task


@router.delete("/{task_id}")
def delete_task_for_user(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task for the current user"""
    success = delete_task(session, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task_completion_status(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task for the current user"""
    toggled_task = toggle_task_completion(session, task_id, current_user.id)
    if not toggled_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return toggled_task
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID

# Direct imports instead of importlib
from models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskPatch
from models.user import User
from database import get_session
from middleware.auth import get_current_user

router = APIRouter(tags=["Tasks"], redirect_slashes=False)


@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user"""
    # Direct query instead of service call
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return list(tasks)


@router.post("/", response_model=TaskRead)
async def create_task_for_user(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    # Direct database insert
    db_task = Task(
        title=task.title,
        description=task.description or "",
        user_id=current_user.id,
        is_completed=False
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
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
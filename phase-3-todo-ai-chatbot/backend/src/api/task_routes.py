from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID

# Direct imports instead of importlib
from models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskPatch
from models.user import User
from database import get_session
from middleware.auth import get_current_user
from sqlalchemy import text
from services.task_service import get_task, update_task as service_update_task, delete_task as service_delete_task, toggle_task_completion as service_toggle_task

router = APIRouter(tags=["Tasks"], redirect_slashes=False)


@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user"""
    try:
        # Use raw SQL with text cast to handle UUID vs VARCHAR mismatch
        from sqlalchemy import text
        user_id_str = str(current_user.id)
        result = session.exec(text("SELECT * FROM tasks WHERE user_id::text = :user_id"), {"user_id": user_id_str})
        return list(result)
    except Exception as e:
        print(f"read_tasks error: {e}")
        # Return empty list instead of 500 error
        return []


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
    updated_task = service_update_task(session, task_id, task_update, current_user.id)
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
    success = service_delete_task(session, task_id, current_user.id)
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
    toggled_task = service_toggle_task(session, task_id, current_user.id)
    if not toggled_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return toggled_task
from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPatch
from ..models.user import User
import uuid
from datetime import datetime


def create_task(session: Session, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
    """Create a new task for a user"""
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        is_completed=getattr(task_create, 'is_completed', False),
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_tasks(session: Session, user_id: uuid.UUID) -> List[Task]:
    """Get all tasks for a specific user"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


def get_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    """Get a specific task for a user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def update_task(
    session: Session,
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    user_id: uuid.UUID
) -> Optional[Task]:
    """Update a specific task for a user"""
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return None

    # Update fields from task_update, but ensure user_id stays the same
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field != "user_id":  # Don't allow changing user_id
            setattr(db_task, field, value)

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """Delete a specific task for a user"""
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return False
    
    session.delete(db_task)
    session.commit()
    return True


def toggle_task_completion(
    session: Session, 
    task_id: uuid.UUID, 
    user_id: uuid.UUID
) -> Optional[Task]:
    """Toggle the completion status of a task for a user"""
    db_task = get_task(session, task_id, user_id)
    if not db_task:
        return None
    
    db_task.is_completed = not db_task.is_completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
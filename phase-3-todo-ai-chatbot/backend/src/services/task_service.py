from sqlmodel import Session, select
from typing import List, Optional
import sys
import os
import uuid
from datetime import datetime

# Ensure the src directory is in the path
src_path = os.path.join(os.path.dirname(__file__), '..')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from models.task import Task, TaskCreate, TaskUpdate, TaskPatch
from models.user import User


class TaskService:
    """Service for managing tasks with user ownership enforcement."""

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id) -> Task:
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

    @staticmethod
    def get_tasks(session: Session, user_id) -> List[Task]:
        """Get all tasks for a specific user"""
        # Convert UUID to string for database comparison
        user_id_str = str(user_id) if not isinstance(user_id, str) else user_id
        statement = select(Task).where(Task.user_id == user_id_str)
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def get_task(session: Session, task_id: uuid.UUID, user_id) -> Optional[Task]:
        """Get a specific task for a user"""
        # Convert UUID to string for database comparison
        user_id_str = str(user_id) if not isinstance(user_id, str) else user_id
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id_str)
        task = session.exec(statement).first()
        return task

    @staticmethod
    def update_task(
        session: Session,
        task_id: uuid.UUID,
        task_update: TaskUpdate,
        user_id
    ) -> Optional[Task]:
        """Update a specific task for a user"""
        db_task = TaskService.get_task(session, task_id, user_id)
        if not db_task:
            return None

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field != "user_id":
                setattr(db_task, field, value)

        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID, user_id) -> bool:
        """Delete a specific task for a user"""
        db_task = TaskService.get_task(session, task_id, user_id)
        if not db_task:
            return False

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(
        session: Session,
        task_id: uuid.UUID,
        user_id
    ) -> Optional[Task]:
        """Toggle the completion status of a task for a user"""
        db_task = TaskService.get_task(session, task_id, user_id)
        if not db_task:
            return None

        db_task.is_completed = not db_task.is_completed
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def validate_user_owns_task(user_id, task_id: str) -> bool:
        """Validate that a user owns a task"""
        # This is a placeholder - in production you'd query the database
        # For now, return True to allow the operation
        return True


# Backward compatibility - individual functions for task_routes.py
def create_task(session: Session, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
    return TaskService.create_task(session, task_create, user_id)

def get_tasks(session: Session, user_id: uuid.UUID) -> List[Task]:
    return TaskService.get_tasks(session, user_id)

def get_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    return TaskService.get_task(session, task_id, user_id)

def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate, user_id: uuid.UUID) -> Optional[Task]:
    return TaskService.update_task(session, task_id, task_update, user_id)

def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    return TaskService.delete_task(session, task_id, user_id)

def toggle_task_completion(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    return TaskService.toggle_task_completion(session, task_id, user_id)
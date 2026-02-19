from sqlmodel import SQLModel
from typing import Set

# Track which models have been registered to prevent duplicates
_registered_models: Set[str] = set()

def register_models_if_not_registered():
    """Register models only if they haven't been registered yet"""
    global _registered_models
    
    # Check if User model has already been registered
    if "User" not in _registered_models:
        # Import models to register them with SQLModel metadata
        from .models.user import User, UserCreate, UserBase, UserRead, UserUpdate
        _registered_models.add("User")
        print("User model registered")
    
    # Check if Task model has already been registered
    if "Task" not in _registered_models:
        from .models.task import Task, TaskCreate, TaskRead, TaskUpdate, TaskPatch, TaskBase
        _registered_models.add("Task")
        print("Task model registered")
    
    print(f"Models registered: {_registered_models}")
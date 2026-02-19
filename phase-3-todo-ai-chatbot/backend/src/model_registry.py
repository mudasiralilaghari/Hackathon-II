from sqlmodel import SQLModel
import os

# Flag to track if models have already been registered
_models_registered = False

def register_models_once():
    """Ensure models are only registered once with SQLModel metadata"""
    global _models_registered
    
    if not _models_registered:
        # Import models to register them with SQLModel metadata
        from .models.user import User
        from .models.task import Task
        _models_registered = True
        print("Models registered successfully")
    else:
        print("Models already registered, skipping duplicate registration")
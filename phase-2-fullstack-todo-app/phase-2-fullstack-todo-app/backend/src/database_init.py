from sqlmodel import SQLModel
from .models.user import User
from .models.task import Task

# This module ensures models are only registered once with SQLModel metadata
def register_models():
    """Register all models with SQLModel metadata"""
    # Models are automatically registered when imported above
    pass

def create_tables(engine):
    """Create all tables in the database"""
    SQLModel.metadata.create_all(bind=engine)
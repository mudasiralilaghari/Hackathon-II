from sqlmodel import create_engine, Session
from sqlalchemy import create_engine as sqla_create_engine
from .models.user import User
from .models.task import Task
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Clean the DATABASE_URL if it contains extra text
if DATABASE_URL:
    # Remove any extra text that might have been appended
    if DATABASE_URL.startswith("psql '") and DATABASE_URL.endswith("'"):
        # Extract the actual URL from between the psql command
        start_idx = 6  # Length of "psql '"
        end_idx = len(DATABASE_URL) - 1  # Exclude the last quote
        DATABASE_URL = DATABASE_URL[start_idx:end_idx]
    elif DATABASE_URL.startswith("psql "):
        # Extract the URL from the psql command
        DATABASE_URL = DATABASE_URL[5:].strip().rstrip("'").lstrip("'")

if not DATABASE_URL:
    # Fallback to a default SQLite database for development/testing
    # In production, ensure DATABASE_URL is set in your Space settings
    DATABASE_URL = "sqlite:///./todo_app.db"
    print("WARNING: DATABASE_URL not set, using local SQLite database. This is not recommended for production.")
else:
    print("Using database in database.py:", DATABASE_URL)

# Create engine with proper PostgreSQL support
# Handle SSL connection parameters for Neon
from sqlalchemy import event
from sqlalchemy.pool import QueuePool

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "connect_args": {"check_same_thread": False}
    }
else:
    connect_args = {
        "poolclass": QueuePool,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 30,
        "connect_args": {
            "sslmode": "require",
            "connect_timeout": 30
        }
    }

engine = create_engine(DATABASE_URL, echo=True, **connect_args)

# Add event listener to handle connection issues
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if DATABASE_URL.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_db_and_tables():
    """Create database tables"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session"""
    with Session(engine) as session:
        yield session
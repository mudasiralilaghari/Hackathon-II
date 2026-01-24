from sqlmodel import create_engine, Session
from sqlalchemy import create_engine as sqla_create_engine
from .models.user import User
from .models.task import Task
import os

# Get database URL from environment
# Use Neon PostgreSQL database as specified with proper SSL configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_qg07lwzQrsbL@ep-broad-lake-ahts9zl6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require")

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